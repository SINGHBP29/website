from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
import random
import json
import smtplib
from email.mime.text import MIMEText

import vote
# Mock Databases
db_voters = [
    {"voter_id": "V123", "name": "Rajesh Kumar", "phone": "9876543210", "aadhaar": "1234-5678-9101", "constituency": "Delhi-01", "has_voted": False},
    {"voter_id": "V124", "name": "Meera Sharma", "phone": "9876543211", "aadhaar": "1234-5678-9102", "constituency": "Delhi-01", "has_voted": False}
]

db_candidates = [
    {"candidate_id": "C001", "name": "Meera Sharma", "party": "People's Party", "constituency": "Delhi-01"},
    {"candidate_id": "C002", "name": "Amit Verma", "party": "Freedom Party", "constituency": "Delhi-01"},
    # Add more candidates as necessary
]

otp_store = {}

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirect authenticated users to the dashboard or main page
    return render(request, 'voting/login.html')  # Render the login page for unauthenticated users

@login_required
def dashboard(request):
    return render(request, 'voting/index.html')  # Render the authenticated user page

@login_required
def index(request):
    return render(request, 'voting/login.html')

# Render Index Page
# def index(request):
#     return render(request, 'voting/index.html')

# OTP Generation
@csrf_exempt
def generate_otp(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        phone = data.get('phone')
        otp = random.randint(100000, 999999)  # Generate 6-digit OTP

        # Store OTP in memory
        otp_store[phone] = otp
        print(f"OTP generated for {phone}: {otp}")

        return JsonResponse({"message": "OTP sent successfully", "otp": otp})
    return JsonResponse({"message": "Invalid request method"}, status=400)
# OTP Verification
@csrf_exempt
def verify_otp(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        contact = data.get('contact')
        input_otp = data.get('otp')

        # Check if the OTP matches
        if otp_store.get(contact) == input_otp:
            return JsonResponse({"message": "OTP verified successfully"})
        return JsonResponse({"message": "Invalid OTP"}, status=400)

    return JsonResponse({"message": "Invalid request method"}, status=400)
# Fetch Candidates
@csrf_exempt
def get_candidates(request):
    if request.method == 'GET':
        constituency = request.GET.get('constituency')
        if not constituency:
            return JsonResponse({"message": "Constituency is required"}, status=400)

        candidates = [c for c in db_candidates if c['constituency'] == constituency]
        return JsonResponse(candidates, safe=False)

# Submit Vote
@csrf_exempt
def submit_vote(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        voter_id = data.get('voter_id')
        candidate_id = data.get('candidate_id')

        if not voter_id or not candidate_id:
            return JsonResponse({"message": "Voter ID and Candidate ID are required"}, status=400)

        voter = next((voter for voter in db_voters if voter['voter_id'] == voter_id), None)
        if not voter:
            return JsonResponse({"message": "Voter not found"}, status=404)

        if voter['has_voted']:
            return JsonResponse({"message": "You have already voted"}, status=400)

        candidate = next((candidate for candidate in db_candidates if candidate['candidate_id'] == candidate_id), None)
        if not candidate:
            return JsonResponse({"message": "Candidate not found"}, status=404)

        # Check vote count limit
        # Assuming each candidate has a limit of 1 vote per user
        # Modify the logic here if needed based on your requirements
        if candidate.get('vote_count', 0) >= 1:
            return JsonResponse({"message": "You are not eligible to vote for this candidate. Maximum votes already cast."}, status=400)

        # Record the vote
        candidate['vote_count'] = candidate.get('vote_count', 0) + 1
        voter['has_voted'] = True
        
        return JsonResponse({"message": "Vote recorded successfully"})

    return JsonResponse({"message": "Invalid request method"}, status=405)

def admin_stats(request):
    if request.method == 'GET':
        constituency = request.GET.get('constituency')
        if not constituency:
            return JsonResponse({"message": "Constituency is required"}, status=400)

        total_voters = len([v for v in db_voters if v['constituency'] == constituency])
        voted = len([v for v in db_voters if v['constituency'] == constituency and v['has_voted']])
        pending = total_voters - voted

        # candidate_votes = {}
        # for c in db_candidates:
        #     if c['constituency'] == constituency:
        #         # Change: Use 'candidate_id' and 'has_voted' fields to calculate votes
        #         votes = sum(1 for v in db_voters if v['candidate_id'] == c['candidate_id'] and v['has_voted'])
        #         candidate_votes[c['candidate_id']] = {'name': c['name'], 'vote_count': votes}

        return JsonResponse({
            "total_voters": total_voters,
            "voted": voted,
            "pending": pending,
            # "candidate_votes": candidate_votes,
        })