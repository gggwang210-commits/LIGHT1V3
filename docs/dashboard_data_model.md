# Dashboard Data Model

All values below are synthetic examples for planning and public portfolio use.

## Member

- Fields: `id`, `createdAt`, `updatedAt`, `status`, `ownerRole`, `notes`; entity-specific planning fields may include `displayName`, `score`, `trend`, `sessionId`, `memberId`, `trainerId`, `amount`, `consentType`, or `action`.
- Example values: `member_001`, `2026-07-06T09:00:00Z`, `Good`, `Synthetic Center A`, `trainer-reviewed wellness reference`.
- Privacy level: high.
- Who can access: Member self, assigned Trainer, authorized AdminUser.
- Notes: Use synthetic IDs and masked labels only; do not store real personal data, clinical records, or public media assets in this repository.

## Trainer

- Fields: `id`, `createdAt`, `updatedAt`, `status`, `ownerRole`, `notes`; entity-specific planning fields may include `displayName`, `score`, `trend`, `sessionId`, `memberId`, `trainerId`, `amount`, `consentType`, or `action`.
- Example values: `trainer_001`, `2026-07-06T09:00:00Z`, `Good`, `Synthetic Center A`, `trainer-reviewed wellness reference`.
- Privacy level: medium.
- Who can access: Trainer and AdminUser.
- Notes: Use synthetic IDs and masked labels only; do not store real personal data, clinical records, or public media assets in this repository.

## AdminUser

- Fields: `id`, `createdAt`, `updatedAt`, `status`, `ownerRole`, `notes`; entity-specific planning fields may include `displayName`, `score`, `trend`, `sessionId`, `memberId`, `trainerId`, `amount`, `consentType`, or `action`.
- Example values: `adminuser_001`, `2026-07-06T09:00:00Z`, `Good`, `Synthetic Center A`, `trainer-reviewed wellness reference`.
- Privacy level: medium.
- Who can access: authorized AdminUser only.
- Notes: Use synthetic IDs and masked labels only; do not store real personal data, clinical records, or public media assets in this repository.

## Center

- Fields: `id`, `createdAt`, `updatedAt`, `status`, `ownerRole`, `notes`; entity-specific planning fields may include `displayName`, `score`, `trend`, `sessionId`, `memberId`, `trainerId`, `amount`, `consentType`, or `action`.
- Example values: `center_001`, `2026-07-06T09:00:00Z`, `Good`, `Synthetic Center A`, `trainer-reviewed wellness reference`.
- Privacy level: low.
- Who can access: Trainer and AdminUser.
- Notes: Use synthetic IDs and masked labels only; do not store real personal data, clinical records, or public media assets in this repository.

## Session

- Fields: `id`, `createdAt`, `updatedAt`, `status`, `ownerRole`, `notes`; entity-specific planning fields may include `displayName`, `score`, `trend`, `sessionId`, `memberId`, `trainerId`, `amount`, `consentType`, or `action`.
- Example values: `session_001`, `2026-07-06T09:00:00Z`, `Good`, `Synthetic Center A`, `trainer-reviewed wellness reference`.
- Privacy level: medium.
- Who can access: Trainer and AdminUser.
- Notes: Use synthetic IDs and masked labels only; do not store real personal data, clinical records, or public media assets in this repository.

## ExerciseLog

- Fields: `id`, `createdAt`, `updatedAt`, `status`, `ownerRole`, `notes`; entity-specific planning fields may include `displayName`, `score`, `trend`, `sessionId`, `memberId`, `trainerId`, `amount`, `consentType`, or `action`.
- Example values: `exerciselog_001`, `2026-07-06T09:00:00Z`, `Good`, `Synthetic Center A`, `trainer-reviewed wellness reference`.
- Privacy level: medium.
- Who can access: Trainer and AdminUser.
- Notes: Use synthetic IDs and masked labels only; do not store real personal data, clinical records, or public media assets in this repository.

## PainResponse

- Fields: `id`, `createdAt`, `updatedAt`, `status`, `ownerRole`, `notes`; entity-specific planning fields may include `displayName`, `score`, `trend`, `sessionId`, `memberId`, `trainerId`, `amount`, `consentType`, or `action`.
- Example values: `painresponse_001`, `2026-07-06T09:00:00Z`, `Good`, `Synthetic Center A`, `trainer-reviewed wellness reference`.
- Privacy level: high.
- Who can access: Member self, assigned Trainer, authorized AdminUser.
- Notes: Use synthetic IDs and masked labels only; do not store real personal data, clinical records, or public media assets in this repository.

## RPERecord

- Fields: `id`, `createdAt`, `updatedAt`, `status`, `ownerRole`, `notes`; entity-specific planning fields may include `displayName`, `score`, `trend`, `sessionId`, `memberId`, `trainerId`, `amount`, `consentType`, or `action`.
- Example values: `rperecord_001`, `2026-07-06T09:00:00Z`, `Good`, `Synthetic Center A`, `trainer-reviewed wellness reference`.
- Privacy level: medium.
- Who can access: Trainer and AdminUser.
- Notes: Use synthetic IDs and masked labels only; do not store real personal data, clinical records, or public media assets in this repository.

## PostureReference

- Fields: `id`, `createdAt`, `updatedAt`, `status`, `ownerRole`, `notes`; entity-specific planning fields may include `displayName`, `score`, `trend`, `sessionId`, `memberId`, `trainerId`, `amount`, `consentType`, or `action`.
- Example values: `posturereference_001`, `2026-07-06T09:00:00Z`, `Good`, `Synthetic Center A`, `trainer-reviewed wellness reference`.
- Privacy level: medium.
- Who can access: Trainer and AdminUser.
- Notes: Use synthetic IDs and masked labels only; do not store real personal data, clinical records, or public media assets in this repository.

## ShootingQC

- Fields: `id`, `createdAt`, `updatedAt`, `status`, `ownerRole`, `notes`; entity-specific planning fields may include `displayName`, `score`, `trend`, `sessionId`, `memberId`, `trainerId`, `amount`, `consentType`, or `action`.
- Example values: `shootingqc_001`, `2026-07-06T09:00:00Z`, `Good`, `Synthetic Center A`, `trainer-reviewed wellness reference`.
- Privacy level: medium.
- Who can access: Trainer and AdminUser.
- Notes: Use synthetic IDs and masked labels only; do not store real personal data, clinical records, or public media assets in this repository.

## QSScore

- Fields: `id`, `createdAt`, `updatedAt`, `status`, `ownerRole`, `notes`; entity-specific planning fields may include `displayName`, `score`, `trend`, `sessionId`, `memberId`, `trainerId`, `amount`, `consentType`, or `action`.
- Example values: `qsscore_001`, `2026-07-06T09:00:00Z`, `Good`, `Synthetic Center A`, `trainer-reviewed wellness reference`.
- Privacy level: low.
- Who can access: Trainer and AdminUser.
- Notes: Use synthetic IDs and masked labels only; do not store real personal data, clinical records, or public media assets in this repository.

## JATCScore

- Fields: `id`, `createdAt`, `updatedAt`, `status`, `ownerRole`, `notes`; entity-specific planning fields may include `displayName`, `score`, `trend`, `sessionId`, `memberId`, `trainerId`, `amount`, `consentType`, or `action`.
- Example values: `jatcscore_001`, `2026-07-06T09:00:00Z`, `Good`, `Synthetic Center A`, `trainer-reviewed wellness reference`.
- Privacy level: low.
- Who can access: Trainer and AdminUser.
- Notes: Use synthetic IDs and masked labels only; do not store real personal data, clinical records, or public media assets in this repository.

## Report

- Fields: `id`, `createdAt`, `updatedAt`, `status`, `ownerRole`, `notes`; entity-specific planning fields may include `displayName`, `score`, `trend`, `sessionId`, `memberId`, `trainerId`, `amount`, `consentType`, or `action`.
- Example values: `report_001`, `2026-07-06T09:00:00Z`, `Good`, `Synthetic Center A`, `trainer-reviewed wellness reference`.
- Privacy level: medium.
- Who can access: Trainer and AdminUser.
- Notes: Use synthetic IDs and masked labels only; do not store real personal data, clinical records, or public media assets in this repository.

## Feedback

- Fields: `id`, `createdAt`, `updatedAt`, `status`, `ownerRole`, `notes`; entity-specific planning fields may include `displayName`, `score`, `trend`, `sessionId`, `memberId`, `trainerId`, `amount`, `consentType`, or `action`.
- Example values: `feedback_001`, `2026-07-06T09:00:00Z`, `Good`, `Synthetic Center A`, `trainer-reviewed wellness reference`.
- Privacy level: medium.
- Who can access: Trainer and AdminUser.
- Notes: Use synthetic IDs and masked labels only; do not store real personal data, clinical records, or public media assets in this repository.

## Reservation

- Fields: `id`, `createdAt`, `updatedAt`, `status`, `ownerRole`, `notes`; entity-specific planning fields may include `displayName`, `score`, `trend`, `sessionId`, `memberId`, `trainerId`, `amount`, `consentType`, or `action`.
- Example values: `reservation_001`, `2026-07-06T09:00:00Z`, `Good`, `Synthetic Center A`, `trainer-reviewed wellness reference`.
- Privacy level: medium.
- Who can access: Trainer and AdminUser.
- Notes: Use synthetic IDs and masked labels only; do not store real personal data, clinical records, or public media assets in this repository.

## Payment

- Fields: `id`, `createdAt`, `updatedAt`, `status`, `ownerRole`, `notes`; entity-specific planning fields may include `displayName`, `score`, `trend`, `sessionId`, `memberId`, `trainerId`, `amount`, `consentType`, or `action`.
- Example values: `payment_001`, `2026-07-06T09:00:00Z`, `Good`, `Synthetic Center A`, `trainer-reviewed wellness reference`.
- Privacy level: medium.
- Who can access: Trainer and AdminUser.
- Notes: Use synthetic IDs and masked labels only; do not store real personal data, clinical records, or public media assets in this repository.

## Message

- Fields: `id`, `createdAt`, `updatedAt`, `status`, `ownerRole`, `notes`; entity-specific planning fields may include `displayName`, `score`, `trend`, `sessionId`, `memberId`, `trainerId`, `amount`, `consentType`, or `action`.
- Example values: `message_001`, `2026-07-06T09:00:00Z`, `Good`, `Synthetic Center A`, `trainer-reviewed wellness reference`.
- Privacy level: high.
- Who can access: Member self, assigned Trainer, authorized AdminUser.
- Notes: Use synthetic IDs and masked labels only; do not store real personal data, clinical records, or public media assets in this repository.

## Consent

- Fields: `id`, `createdAt`, `updatedAt`, `status`, `ownerRole`, `notes`; entity-specific planning fields may include `displayName`, `score`, `trend`, `sessionId`, `memberId`, `trainerId`, `amount`, `consentType`, or `action`.
- Example values: `consent_001`, `2026-07-06T09:00:00Z`, `Good`, `Synthetic Center A`, `trainer-reviewed wellness reference`.
- Privacy level: high.
- Who can access: Member self, assigned Trainer, authorized AdminUser.
- Notes: Use synthetic IDs and masked labels only; do not store real personal data, clinical records, or public media assets in this repository.

## AuditLog

- Fields: `id`, `createdAt`, `updatedAt`, `status`, `ownerRole`, `notes`; entity-specific planning fields may include `displayName`, `score`, `trend`, `sessionId`, `memberId`, `trainerId`, `amount`, `consentType`, or `action`.
- Example values: `auditlog_001`, `2026-07-06T09:00:00Z`, `Good`, `Synthetic Center A`, `trainer-reviewed wellness reference`.
- Privacy level: high.
- Who can access: authorized AdminUser only.
- Notes: Use synthetic IDs and masked labels only; do not store real personal data, clinical records, or public media assets in this repository.

## ReviewQueueItem

- Fields: `id`, `createdAt`, `updatedAt`, `status`, `ownerRole`, `notes`; entity-specific planning fields may include `displayName`, `score`, `trend`, `sessionId`, `memberId`, `trainerId`, `amount`, `consentType`, or `action`.
- Example values: `reviewqueueitem_001`, `2026-07-06T09:00:00Z`, `Good`, `Synthetic Center A`, `trainer-reviewed wellness reference`.
- Privacy level: medium.
- Who can access: Trainer and AdminUser.
- Notes: Use synthetic IDs and masked labels only; do not store real personal data, clinical records, or public media assets in this repository.
