/**
 * LIGHT ONE survey external integrations.
 *
 * Add this file to the existing Apps Script project. Do not replace the
 * production doPost(), Sheet writer, PDF generator, or email sender.
 * Call syncExternalSystems_(normalizedRecord) only after the primary Google
 * workflow has written the response successfully.
 */

const LIGHT_ONE_INTEGRATION_DEFAULTS = Object.freeze({
  AIRTABLE_RESPONSES_TABLE: 'Responses',
  AIRTABLE_LOG_TABLE: 'Integration Log',
  SOURCE_VERSION: '2026-07',
  MAX_ATTEMPTS: 3,
  SLACK_INCLUDE_PDF_LINK: false
});

/**
 * Best-effort secondary synchronization. A secondary destination failure must
 * not delete or roll back the Google Sheet/PDF source of truth.
 *
 * @param {Object} record normalized record matching survey-response.schema.json
 * @return {Object} destination results
 */
function syncExternalSystems_(record) {
  const props = PropertiesService.getScriptProperties();
  if (String(props.getProperty('INTEGRATIONS_ENABLED')).toLowerCase() !== 'true') {
    return { enabled: false, results: [] };
  }

  validateIntegrationRecord_(record);
  const safe = buildOperationsRecord_(record);
  const results = [];

  results.push(runDestination_('Airtable', function () {
    return upsertAirtableResponse_(safe, props);
  }));

  results.push(runDestination_('Slack', function () {
    return sendSlackStatus_(safe, props);
  }));

  return { enabled: true, responseId: safe.responseId, results: results };
}

function runDestination_(destination, operation) {
  try {
    const response = operation();
    return { destination: destination, status: 'SUCCESS', response: response };
  } catch (error) {
    console.error(JSON.stringify({
      destination: destination,
      status: 'FAILED',
      error: redactError_(error && error.message ? error.message : String(error))
    }));
    return {
      destination: destination,
      status: 'FAILED',
      error: redactError_(error && error.message ? error.message : String(error))
    };
  }
}

function validateIntegrationRecord_(record) {
  if (!record || typeof record !== 'object') throw new Error('record is required');
  if (!record.response_id) throw new Error('response_id is required');
  if (['owner', 'coach', 'member'].indexOf(record.role) === -1) {
    throw new Error('unsupported role');
  }
  if (record.consent !== true) throw new Error('consent is required');
  if (!record.answers || Object.keys(record.answers).length !== 15) {
    throw new Error('exactly 15 answers are required');
  }
}

/**
 * Removes contact fields and free-form comments before external operations.
 */
function buildOperationsRecord_(record) {
  return {
    responseId: String(record.response_id),
    role: roleLabel_(record.role),
    receivedAt: String(record.received_at || new Date().toISOString()),
    consent: record.consent === true,
    answerSummary: String(record.answer_summary || '').slice(0, 12000),
    pdfUrl: record.pdf && record.pdf.url ? String(record.pdf.url) : '',
    emailStatus: String(record.email_status || 'PENDING'),
    processStatus: String(record.process_status || 'RECEIVED'),
    retryCount: Number(record.retry_count || 0),
    hasContact: Boolean(record.contact && (
      record.contact.name || record.contact.organization ||
      record.contact.reply_email || record.contact.phone
    )),
    errorMessage: redactError_(record.error_message || ''),
    updatedAt: String(record.updated_at || new Date().toISOString()),
    sourceVersion: String(record.source_version || LIGHT_ONE_INTEGRATION_DEFAULTS.SOURCE_VERSION)
  };
}

function roleLabel_(role) {
  return ({ owner: '센터장·원장', coach: '트레이너', member: '회원' })[role];
}

function upsertAirtableResponse_(safe, props) {
  const pat = requireProperty_(props, 'AIRTABLE_PAT');
  const baseId = requireProperty_(props, 'AIRTABLE_BASE_ID');
  const table = props.getProperty('AIRTABLE_RESPONSES_TABLE') ||
    LIGHT_ONE_INTEGRATION_DEFAULTS.AIRTABLE_RESPONSES_TABLE;
  const url = 'https://api.airtable.com/v0/' + encodeURIComponent(baseId) + '/' + encodeURIComponent(table);

  const payload = {
    performUpsert: { fieldsToMergeOn: ['Response ID'] },
    records: [{
      fields: {
        'Response ID': safe.responseId,
        'Role': safe.role,
        'Received At': safe.receivedAt,
        'Consent': safe.consent,
        'Answer Summary': safe.answerSummary,
        'PDF URL': safe.pdfUrl || null,
        'Email Status': safe.emailStatus,
        'Process Status': safe.processStatus,
        'Retry Count': safe.retryCount,
        'Has Contact': safe.hasContact,
        'Error Message': safe.errorMessage,
        'Updated At': safe.updatedAt,
        'Source Version': safe.sourceVersion
      }
    }]
  };

  const result = fetchJsonWithRetry_(url, {
    method: 'post',
    contentType: 'application/json',
    headers: { Authorization: 'Bearer ' + pat },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  });

  return { statusCode: result.statusCode, recordCount: (result.body.records || []).length };
}

function sendSlackStatus_(safe, props) {
  const webhook = requireProperty_(props, 'SLACK_WEBHOOK_URL');
  const includePdf = String(props.getProperty('SLACK_INCLUDE_PDF_LINK')).toLowerCase() === 'true';
  const statusEmoji = safe.processStatus === 'COMPLETED' ? ':white_check_mark:' :
    (safe.processStatus === 'FAILED' ? ':warning:' : ':hourglass_flowing_sand:');

  const lines = [
    statusEmoji + ' *LIGHT ONE 설문 처리 상태*',
    '• 응답 ID: `' + safe.responseId + '`',
    '• 역할: ' + safe.role,
    '• 처리: `' + safe.processStatus + '`',
    '• 이메일: `' + safe.emailStatus + '`',
    '• 업데이트: ' + safe.updatedAt
  ];
  if (includePdf && safe.pdfUrl) lines.push('• PDF: ' + safe.pdfUrl);
  if (safe.errorMessage) lines.push('• 오류: `' + safe.errorMessage.slice(0, 240) + '`');

  const result = fetchTextWithRetry_(webhook, {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify({ text: lines.join('\n') }),
    muteHttpExceptions: true
  });
  return { statusCode: result.statusCode };
}

function fetchJsonWithRetry_(url, options) {
  const result = fetchTextWithRetry_(url, options);
  let body = {};
  try { body = result.text ? JSON.parse(result.text) : {}; } catch (ignore) {}
  return { statusCode: result.statusCode, body: body };
}

function fetchTextWithRetry_(url, options) {
  let lastError = null;
  for (let attempt = 1; attempt <= LIGHT_ONE_INTEGRATION_DEFAULTS.MAX_ATTEMPTS; attempt += 1) {
    try {
      const response = UrlFetchApp.fetch(url, options);
      const statusCode = response.getResponseCode();
      const text = response.getContentText();
      if (statusCode >= 200 && statusCode < 300) {
        return { statusCode: statusCode, text: text };
      }
      if (statusCode < 429 && statusCode < 500) {
        throw new Error('non-retryable destination status ' + statusCode);
      }
      lastError = new Error('destination status ' + statusCode);
    } catch (error) {
      lastError = error;
    }
    if (attempt < LIGHT_ONE_INTEGRATION_DEFAULTS.MAX_ATTEMPTS) {
      Utilities.sleep(Math.pow(2, attempt - 1) * 1000);
    }
  }
  throw lastError || new Error('destination request failed');
}

function requireProperty_(props, key) {
  const value = props.getProperty(key);
  if (!value) throw new Error('missing Script Property: ' + key);
  return value;
}

function redactError_(value) {
  return String(value || '')
    .replace(/[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/gi, '[EMAIL]')
    .replace(/(?:\+?82[- ]?)?0?1[016789][ -]?\d{3,4}[ -]?\d{4}/g, '[PHONE]')
    .replace(/Bearer\s+[A-Za-z0-9._-]+/gi, 'Bearer [REDACTED]')
    .replace(/hooks\.slack\.com\/services\/[A-Za-z0-9/_-]+/gi, 'hooks.slack.com/services/[REDACTED]')
    .slice(0, 1000);
}

