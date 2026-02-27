#!/usr/bin/env python
"""Run this after migrations to create admin and sample data."""
import os, sys, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nck_revision.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from accounts.models import CustomUser
from questions.models import Category, Question

# Create superuser admin
if not CustomUser.objects.filter(username='admin').exists():
    CustomUser.objects.create_superuser(
        username='admin', email='admin@nckprep.co.ke',
        password='admin1234', is_approved=True
    )
    print("✅ Admin created: username=admin, password=admin1234")

# Sample BSN categories
bsn_cats = [
    ('Medical-Surgical Nursing', 'BSN'),
    ('Pharmacology', 'BSN'),
    ('Anatomy & Physiology', 'BSN'),
    ('Community Health', 'BSN'),
    ('Mental Health Nursing', 'BSN'),
]
for name, course in bsn_cats:
    Category.objects.get_or_create(name=name, course=course)

# Sample KRCHN categories
krchn_cats = [
    ('Fundamental Nursing', 'KRCHN'),
    ('Maternal & Child Health', 'KRCHN'),
    ('Community Health', 'KRCHN'),
    ('Clinical Medicine', 'KRCHN'),
]
for name, course in krchn_cats:
    Category.objects.get_or_create(name=name, course=course)

# Sample questions
samples = [
    {
        'cat': ('Medical-Surgical Nursing', 'BSN'),
        'q': 'What is the normal adult resting heart rate?',
        'a': '60–100 beats per minute (bpm)',
        'exp': 'The normal adult resting heart rate ranges from 60 to 100 bpm. Rates below 60 bpm indicate bradycardia; above 100 bpm indicates tachycardia.',
        'diff': 'easy'
    },
    {
        'cat': ('Medical-Surgical Nursing', 'BSN'),
        'q': 'Which electrolyte imbalance is most commonly associated with cardiac arrhythmias?',
        'a': 'Hypokalemia (low potassium)',
        'exp': 'Potassium is critical for cardiac muscle function. Hypokalemia can cause life-threatening dysrhythmias including ventricular fibrillation.',
        'diff': 'medium'
    },
    {
        'cat': ('Pharmacology', 'BSN'),
        'q': 'What is the antidote for heparin overdose?',
        'a': 'Protamine sulfate',
        'exp': 'Protamine sulfate neutralizes heparin by binding to it and forming a stable complex that has no anticoagulant activity.',
        'diff': 'medium'
    },
    {
        'cat': ('Pharmacology', 'BSN'),
        'q': 'What is the antidote for warfarin (Coumadin) overdose?',
        'a': 'Vitamin K (phytonadione)',
        'exp': 'Warfarin inhibits Vitamin K-dependent clotting factors. Vitamin K reverses this effect. Fresh frozen plasma may also be given for immediate reversal.',
        'diff': 'medium'
    },
    {
        'cat': ('Anatomy & Physiology', 'BSN'),
        'q': 'Which chamber of the heart pumps oxygenated blood to the systemic circulation?',
        'a': 'Left ventricle',
        'exp': 'The left ventricle is the most muscular chamber and pumps oxygenated blood through the aorta to the entire body.',
        'diff': 'easy'
    },
    {
        'cat': ('Fundamental Nursing', 'KRCHN'),
        'q': 'What does the acronym SOAP stand for in nursing documentation?',
        'a': 'Subjective, Objective, Assessment, Plan',
        'exp': 'SOAP is a structured method of documentation. S=patient complaints, O=measurable findings, A=nurse assessment/diagnosis, P=care plan.',
        'diff': 'easy'
    },
    {
        'cat': ('Fundamental Nursing', 'KRCHN'),
        'q': 'What is the correct hand hygiene duration recommended by WHO?',
        'a': '20–30 seconds for handrubbing with alcohol; 40–60 seconds for handwashing with soap and water',
        'exp': 'WHO guidelines specify specific durations to ensure effective decontamination. Handwashing takes longer due to the mechanical action needed.',
        'diff': 'easy'
    },
    {
        'cat': ('Maternal & Child Health', 'KRCHN'),
        'q': 'What is the APGAR score assessed at 1 and 5 minutes after birth?',
        'a': 'Appearance (color), Pulse (heart rate), Grimace (reflex), Activity (muscle tone), Respiration — scored 0-2 each, total 0-10',
        'exp': 'APGAR score ≥7 is normal. 4-6 requires close monitoring. <4 requires immediate resuscitation. The 5-minute score is more predictive of outcomes.',
        'diff': 'medium'
    },
    {
        'cat': ('Community Health', 'BSN'),
        'q': 'What are the three levels of disease prevention?',
        'a': 'Primary (preventing disease), Secondary (early detection/screening), Tertiary (reducing disability/rehabilitation)',
        'exp': 'Primary: vaccinations, health education. Secondary: mammograms, BP screening. Tertiary: cardiac rehab, physiotherapy after stroke.',
        'diff': 'medium'
    },
    {
        'cat': ('Mental Health Nursing', 'BSN'),
        'q': 'What is the priority nursing intervention when caring for a suicidal patient?',
        'a': 'Ensure patient safety by removing harmful objects and maintaining close observation (1:1 supervision)',
        'exp': 'Safety is the highest priority (Maslow). The nurse must maintain a therapeutic relationship while implementing suicide precautions including removing ligature risks.',
        'diff': 'hard'
    },
]

for item in samples:
    cat = Category.objects.get(name=item['cat'][0], course=item['cat'][1])
    if not Question.objects.filter(question_text=item['q']).exists():
        Question.objects.create(
            category=cat,
            question_text=item['q'],
            answer=item['a'],
            explanation=item['exp'],
            difficulty=item['diff']
        )

print(f"✅ Setup complete! {Question.objects.count()} questions, {Category.objects.count()} categories")
print("👉 Run: python manage.py runserver")
print("👉 Login at: http://127.0.0.1:8000/accounts/login/")
print("👉 Admin panel: http://127.0.0.1:8000/admin-panel/")
