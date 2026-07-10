from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Member
from pt_sessions.models import MemberSession


@login_required
def member_list(request):
    members = Member.objects.filter(is_active=True).order_by('-registered_at')
    return render(request, 'members/member_list.html', {'members': members})


@login_required
def member_detail(request, pk):
    member = get_object_or_404(Member, pk=pk)
    sessions = MemberSession.objects.filter(member=member).order_by('-created_at')[:10]
    return render(request, 'members/member_detail.html', {
        'member': member,
        'sessions': sessions,
    })


@login_required
def member_create(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        age = request.POST.get('age') or None
        sex = request.POST.get('sex', '')
        goal = request.POST.get('goal', 'posture')
        discomfort_area = request.POST.get('discomfort_area', '')
        memo = request.POST.get('memo', '')
        if not name:
            messages.error(request, '이름을 입력해주세요.')
            return render(request, 'members/member_form.html', {'action': '등록'})
        try:
            trainer_profile = request.user.trainer_profile
        except Exception:
            trainer_profile = None
        Member.objects.create(
            trainer=trainer_profile,
            name=name,
            age=int(age) if age else None,
            sex=sex,
            goal=goal,
            discomfort_area=discomfort_area,
            memo=memo,
        )
        messages.success(request, f'{name} 회원이 등록되었습니다.')
        return redirect('member_list')
    return render(request, 'members/member_form.html', {'action': '등록'})


@login_required
def member_edit(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        member.name = request.POST.get('name', member.name).strip()
        member.age = request.POST.get('age') or None
        member.sex = request.POST.get('sex', member.sex)
        member.goal = request.POST.get('goal', member.goal)
        member.discomfort_area = request.POST.get('discomfort_area', member.discomfort_area)
        member.memo = request.POST.get('memo', member.memo)
        member.save()
        messages.success(request, f'{member.name} 회원 정보가 수정되었습니다.')
        return redirect('member_detail', pk=pk)
    return render(request, 'members/member_form.html', {'action': '수정', 'member': member})
