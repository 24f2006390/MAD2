from flask_restful import fields


company_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'website': fields.String,
    'hr_email': fields.String,
    'hr_phone': fields.String,
    'hq_address': fields.String,
    'tagline': fields.String,
    'industry': fields.String,
    'founded_year': fields.Integer,
    'description': fields.String,
    'no_of_offices': fields.Integer,
    'staff_size': fields.Integer,
    'approval_status': fields.String
}

job_fields = {
    'created_at':fields.String,
    'id': fields.Integer,
    'title': fields.String,
    'location': fields.String,
    'salary': fields.String,
    'experience': fields.String,
    'is_closed': fields.Integer,
    'application_deadline': fields.DateTime(dt_format='iso8601'),
    'description': fields.String,
    'company_id': fields.Integer,
    'company':fields.Nested(company_fields),
    'approval_status': fields.String , 
    
}


student_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'email_id': fields.String,
    'phone_no': fields.String,
    'cgpa': fields.Float,
    'graduation_year': fields.String,
    'branch': fields.String,
    'degree': fields.String,
    'approval_status': fields.String,
    'photo_path': fields.String,

}

application_fields = {
    'id': fields.Integer,
    'created_at' : fields.DateTime ,   
    'status': fields.String,
    'resume_path': fields.String,
    'why_hire': fields.String,
    'remark': fields.String,
    'student_id': fields.Integer,
    'student':fields.Nested(student_fields),
    'job_id': fields.Integer,
    'job':fields.Nested(job_fields) , 


}

