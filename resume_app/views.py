from django.shortcuts import render, redirect, get_object_or_404
from .models import Resume
from .nlp_utils import extract_text_from_pdf, parse_resume

# 🔹 Scoring function
def calculate_score(parsed_data, job_description):
    score = 0
    jd_words = set(job_description.lower().split())
    resume_text = " ".join(parsed_data.values()).lower()
    matched = sum(1 for word in jd_words if word in resume_text)
    if jd_words:
        score = round((matched / len(jd_words)) * 100, 2)
    return score

def upload_resume(request):
    resumes = Resume.objects.all().order_by("-score")

    if request.method == "POST":
        name = request.POST.get("name")
        job_description = request.POST.get("job_description")
        resume_file = request.FILES.get("resume_file")

        if not resume_file:
            return redirect("upload_resume")

        # PDF → TEXT
        text = extract_text_from_pdf(resume_file)

        # TEXT → SECTIONS
        parsed_data = parse_resume(text)

        # 🔹 Calculate score
        score = calculate_score(parsed_data, job_description)

        # SAVE TO DB
        Resume.objects.create(
            name=name,
            summary=parsed_data.get("summary") or "Not mentioned",
            experience=parsed_data.get("experience") or "Not mentioned",
            education=parsed_data.get("education") or "Not mentioned",
            skills=parsed_data.get("skills") or "Not mentioned",
            score=score,
            resume_file=resume_file
        )

        return redirect("upload_resume")

    return render(request, "upload_resume.html", {"resumes": resumes})


def delete_resume(request, pk):
    resume = get_object_or_404(Resume, id=pk)
    if resume.resume_file:
        resume.resume_file.delete(save=False)
    resume.delete()
    return redirect("upload_resume")
