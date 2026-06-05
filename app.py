from flask import Flask, render_template, request, redirect, session, flash
import pyodbc
import random
import smtplib
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Database Connection
conn = pyodbc.connect(
       f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={os.getenv('DB_SERVER')};"
    f"DATABASE={os.getenv('DB_DATABASE')};"
    f"UID={os.getenv('DB_USERNAME')};"
    f"PWD={os.getenv('DB_PASSWORD')};"
    f"TrustServerCertificate=yes;"
)


@app.route('/')
def home():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT TOP 3 id, title, content, image 
        FROM blogs 
        ORDER BY id DESC
    """)
    blogs = cursor.fetchall()

    return render_template('index.html', blogs=blogs)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/team")
def team():
    return render_template("team.html")

@app.route("/why-us")
def why_us():
    return render_template("why-us.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route('/services/income-tax-litigation')
def income_tax():
    return render_template('services/income-tax.html')

@app.route('/services/civil-law')
def civil_law():
    return render_template('services/civil-law.html')

@app.route('/services/criminal-law')
def criminal_law():
    return render_template('services/criminal-law.html')

@app.route('/services/family-divorce')
def family():
    return render_template('services/family.html')

@app.route('/services/consumer-cases')
def consumer():
    return render_template('services/consumer.html')

@app.route('/services/legal-documentation')
def documentation():
    return render_template('services/documentation.html')

@app.route('/services/gst-services')
def gst():
    return render_template('services/gst.html')

@app.route('/services/epf')
def epf():
    return render_template('services/epf.html')

@app.route('/services/esic')
def esic():
    return render_template('services/esic.html')

@app.route('/services/other')
def other_services():
    return render_template('services/other.html')


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

# ================= ADMIN AUTH =================
@app.route('/admin/login', methods  =['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['username'].strip()
        password = request.form['password'].strip()

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admins WHERE email=?", (email,))
        admin = cursor.fetchone()

        if admin and admin.password == password:
            session['admin'] = email
            return redirect('/admin/dashboard')
        else:
            flash("Invalid Email or Password")

    return render_template('admin/login.html')

# ================= ADMIN DASHBOARD =================
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect('/admin/login')

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM blogs")
    blog_count = cursor.fetchone()[0]

    return render_template('admin/dashboard.html', blog_count=blog_count)
# ================= ADMIN PROFILE =================
@app.route('/admin/profile')
def admin_profile():
    if 'admin' not in session:
        return redirect('/admin/login')

    cursor = conn.cursor()
    cursor.execute("SELECT username, email FROM admins WHERE email=?", (session['admin'],))
    admin = cursor.fetchone()

    if admin is None:
        return "Admin not found in database"

    admin_data = {
        'username': admin[0],
        'email': admin[1]
    }

    return render_template('admin/profile.html', admin=admin_data)

@app.route('/admin/change-email', methods=['GET', 'POST'])
def change_email():
    if 'admin' not in session:
        return redirect('/admin/login')

    if request.method == 'POST':
        new_email = request.form['email']
        current_email = session['admin']

        cursor = conn.cursor()
        cursor.execute("UPDATE admins SET email=? WHERE email=?", (new_email, current_email))
        conn.commit()

        session['admin'] = new_email
        flash("Email updated successfully")
        return redirect('/admin/profile')

    return render_template('admin/change_email.html')


@app.route('/admin/change-password-request', methods=['GET', 'POST'])
def change_password_request():
    if 'admin' not in session:
        return redirect('/admin/login')

    # Redirect directly to forgot password
    session['reset_email'] = session['admin']
    return redirect('admin/forgot-password')


# ================= ADMIN FORGOT PASSWORD =================

from email.mime.text import MIMEText
import smtplib

def send_otp_email(receiver_email, otp):
    sender_email = "swarajdhaskat02@gmail.com"
    app_password = "eeap arji jvhe nxry"

    subject = "Password Reset OTP"
    body = f"Your OTP for password reset is {otp}"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("OTP Email Sent Successfully")
    except Exception as e:
        print("Email error:", e)

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email'].strip()
        otp = str(random.randint(100000, 999999))

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM admins WHERE email=?", (email,))
        admin = cursor.fetchone()

        if not admin:
            flash("Email not found")
            return redirect('/forgot-password')

        cursor.execute("INSERT INTO password_reset (email, otp) VALUES (?, ?)", (email, otp))
        conn.commit()

        # Send OTP to email
        send_otp_email(email, otp)

        session['reset_email'] = email
        flash("OTP sent to your email")
        return redirect('/verify-otp')

    email = session.get('templates/admin')
    return render_template('admin/forgot_password.html', email=email)

# ================= ADMIN VERIFY OTP =================
@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        otp = request.form['otp']
        email = session.get('reset_email')

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM password_reset WHERE email=? AND otp=?", (email, otp))
        record = cursor.fetchone()

        if record:
            session['otp_verified'] = True
            return redirect('/change-password')
        else:
            flash("Invalid OTP")

    return render_template('admin/verify_otp.html')

# ================= CHANGE PASSWORD =================
@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if not session.get('otp_verified'):
        return redirect('/forgot-password')

    if request.method == 'POST':
        new_password = request.form['password']
        email = session.get('reset_email')

        cursor = conn.cursor()
        cursor.execute("UPDATE admins SET password=? WHERE email=?", (new_password, email))
        conn.commit()

        # Clear session
        session.pop('otp_verified', None)
        session.pop('reset_email', None)

        flash("Password Updated Successfully")
        return redirect('/admin/login')

    return render_template('admin/change_password.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('templates/admin', None)
    return redirect('/admin/login')


# =================BLOG PAGE=================
@app.route('/blogs')
def public_blogs():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM blogs ORDER BY id DESC")
    blogs = cursor.fetchall()
    return render_template('admin/blog_page.html', blogs=blogs)

@app.route('/blog/<int:id>')
def blog_detail(id):
    cursor = conn.cursor()

    # ✅ FIXED SELECT
    cursor.execute("""
        SELECT id, title, slug, content, image, status, author
        FROM blogs WHERE id=?
    """, (id,))
    blog = cursor.fetchone()

    # IMAGES
    cursor.execute("SELECT image FROM blog_images WHERE blog_id=?", (id,))
    images = cursor.fetchall()

    # AUTHOR
    author = None
    if blog and blog[6]:
        cursor.execute("SELECT * FROM team WHERE id=?", (blog[6],))
        author = cursor.fetchone()

    return render_template(
        'admin/blog_detail.html',
        blog=blog,
        images=images,
        author=author
    )
# ================= BLOG CRUD =================

@app.route('/admin/blogs')
def blog_list():
    if 'admin' not in session:
        return redirect('/admin/login')

    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    status = request.args.get('status', '')

    per_page = 8
    offset = (page - 1) * per_page

    cursor = conn.cursor()

    query = "SELECT * FROM blogs WHERE 1=1"
    params = []

    if search:
        query += " AND title LIKE ?"
        params.append(f"%{search}%")

    if status:
        query += " AND status = ?"
        params.append(status)

    query += " ORDER BY id DESC OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
    params.extend([offset, per_page])

    cursor.execute(query, params)
    blogs = cursor.fetchall()

    # Count total blogs for pagination
    count_query = "SELECT COUNT(*) FROM blogs WHERE 1=1"
    count_params = []

    if search:
        count_query += " AND title LIKE ?"
        count_params.append(f"%{search}%")

    if status:
        count_query += " AND status = ?"
        count_params.append(status)

    cursor.execute(count_query, count_params)
    total = cursor.fetchone()[0]

    total_pages = (total + per_page - 1) // per_page

    return render_template(
        'admin/blog_list.html',
        blogs=blogs,
        page=page,
        total_pages=total_pages,
        search=search,
        status=status
    )




UPLOAD_FOLDER = 'static/uploads'

@app.route('/admin/add-blog', methods=['GET', 'POST'])
def add_blog():
    if 'admin' not in session:
        return redirect('/admin/login')

    cursor = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        slug = request.form['slug']
        content = request.form['content']
        status = request.form['status']
        author = request.form['author']   # ✅ NEW

        image_file = request.files['image']
        image_name = None

        if image_file and image_file.filename != '':
            image_name = image_file.filename
            image_file.save(os.path.join(UPLOAD_FOLDER, image_name))

        cursor.execute("""
            INSERT INTO blogs (title, slug, content, image, status, author)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, slug, content, image_name, status, author))

        conn.commit()

        cursor.execute("SELECT TOP 1 id FROM blogs ORDER BY id DESC")
        blog_id = cursor.fetchone()[0]

        images = request.files.getlist('images')
        for img in images:
            if img and img.filename != '':
                img_name = img.filename
                img.save(os.path.join(UPLOAD_FOLDER, img_name))

                cursor.execute("""
                    INSERT INTO blog_images (blog_id, image)
                    VALUES (?, ?)
                """, (blog_id, img_name))

        conn.commit()

        return redirect('/admin/blogs')

    # ✅ SEND TEAM DATA
    cursor.execute("SELECT * FROM team")
    team = cursor.fetchall()

    return render_template('admin/add_blog.html', team=team)


@app.route('/admin/edit-blog/<int:id>', methods=['GET', 'POST'])
def edit_blog(id):
    if 'admin' not in session:
        return redirect('/admin/login')

    cursor = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        status = request.form['status']

        image_file = request.files['image']

        if image_file and image_file.filename != '':
            image_name = image_file.filename
            image_file.save(os.path.join(UPLOAD_FOLDER, image_name))

            cursor.execute("""
                UPDATE blogs
                SET title=?, content=?, status=?, image=?
                WHERE id=?
            """, (title, content, status, image_name, id))
        else:
            cursor.execute("""
                UPDATE blogs
                SET title=?, content=?, status=?
                WHERE id=?
            """, (title, content, status, id))

        conn.commit()
        return redirect('/admin/blogs')

    cursor.execute("""
        SELECT id, title, slug, content, image, status
        FROM blogs WHERE id=?
    """, (id,))
    blog = cursor.fetchone()

    cursor.execute("SELECT image FROM blog_images WHERE blog_id=?", (id,))
    images = cursor.fetchall()

    return render_template('admin/edit_blog.html', blog=blog, images=images)

@app.route('/admin/delete-blog/<int:id>')
def delete_blog(id):
    cursor = conn.cursor()

    # First delete images
    cursor.execute("DELETE FROM blog_images WHERE blog_id=?", (id,))

    # Then delete blog
    cursor.execute("DELETE FROM blogs WHERE id=?", (id,))

    conn.commit()

    return redirect('/admin/blogs')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml')

    
if __name__ == "__main__":
    app.run( port=5000, debug=True)
