def generate_complaint(name, phone, date, branch, college, description):
    complaint = f"""
To,
The Principal,
{college}

Subject: Student Complaint

Respected Sir/Madam,

I, {name}, would like to submit a complaint regarding an incident
that occurred on {date} in {branch} branch.

Complaint details:
{description}

Kindly take necessary action.

Contact Number: {phone}

Thank you.
"""
    return complaint
