import os
import pandas as pd
from datetime import datetime, timezone
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

import db

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-this-secret-key-before-deploying')


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper
    
def roles_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            if 'user_id' not in session:
                return redirect(url_for('login'))

            if session.get('role') not in allowed_roles:
                flash("Wala kang permission para gawin ito.", "error")
                return redirect(url_for('dashboard'))

            return f(*args, **kwargs)

        return wrapper
    return decorator

def create_audit_log(action, target="", details=""):

    conn = db.get_conn()

    conn.execute(
        '''
        INSERT INTO audit_logs
        (
            user_id,
            username,
            action,
            target,
            details,
            ip_address,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''',
        (
            session.get('user_id'),
            session.get('username'),
            action,
            target,
            details,
            request.remote_addr,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
    )

    conn.commit()
    conn.close()

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if not session.get('role'):
            flash("Admins lang ang pwedeng gumawa nito.", "error")
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return wrapper


def parse_dt(s):
    return datetime.strptime(s, '%Y-%m-%d %H:%M:%S.%f') if '.' in s else datetime.strptime(s, '%Y-%m-%d %H:%M:%S')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        conn = db.get_conn()
        user = conn.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()
        conn.close()
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('dashboard'))
        flash("Mali ang username o password.", "error")
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():

    if request.method == 'POST':

        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')


        if new_password != confirm_password:
            flash("Hindi magkapareho ang bagong password.", "error")
            return redirect(url_for('change_password'))


        conn = db.get_conn()

        user = conn.execute(
            'SELECT * FROM user WHERE id = ?',
            (session['user_id'],)
        ).fetchone()


        if not check_password_hash(user['password_hash'], old_password):
            flash("Mali ang current password.", "error")
            conn.close()
            return redirect(url_for('change_password'))


        conn.execute(
            '''
            UPDATE user
            SET password_hash = ?,
                updated_at = ?
            WHERE id = ?
            ''',
            (
                generate_password_hash(new_password),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                session['user_id']
            )
        )


        conn.commit()
        conn.close()

        flash("Password successfully changed.", "success")

        return redirect(url_for('dashboard'))


    return render_template('change_password.html')

@app.route('/')
@login_required
def dashboard():

    conn = db.get_conn()
    module = request.args.get('module', 'MPS')    

    sites = conn.execute(
        'SELECT * FROM site ORDER BY name'
    ).fetchall()


    site_id = request.args.get('site_id', type=int)

    active_site = None


    if site_id:
        active_site = conn.execute(
            'SELECT * FROM site WHERE id = ?',
            (site_id,)
        ).fetchone()


    if not active_site and sites:
        active_site = sites[0]



    # ==========================
    # AGENT CHECKING DASHBOARD
    # ==========================

    if module == "AGENT":


        kpi_rows = conn.execute("""
            SELECT
                AGENT,
                DEPOSIT,
                WITHDRAWAL,
                NET_DEPOSIT,
                PLAYER_COUNT,
                VTO,
                WINLOSS,
                COMMS,
                "COMMS%",
                OVER_ALL

            FROM kpi_data

            ORDER BY OVER_ALL DESC

        """).fetchall()



        kpi = []

        rank = 1


        for row in kpi_rows:

            kpi.append({

                "position": rank,
                "agent": row["AGENT"],
                "deposit": row["DEPOSIT"],
                "withdrawal": row["WITHDRAWAL"],
                "net_deposit": row["NET_DEPOSIT"],
                "player_count": row["PLAYER_COUNT"],
                "vto": row["VTO"],
                "winloss": row["WINLOSS"],
                "comms": row["COMMS"],
                "comms_percent": row["COMMS%"],
                "overall": row["OVER_ALL"]

            })


            rank += 1



        conn.close()


        return render_template(
            "agentdashboard.html",

            sites=sites,

            active_site=active_site,

            kpi=kpi,

            username=session.get("username"),

            module=module
        )



    # ==========================
    # MPS DEFAULT DASHBOARD
    # ==========================


    all_records = conn.execute(

        'SELECT * FROM record WHERE site_id = ? ORDER BY created_at DESC',

        (active_site['id'],)

    ).fetchall()


    from collections import Counter


    ip_counts = Counter(
        r['ip_address']
        for r in all_records
        if r['ip_address']
    )


    acct_counts = Counter(
        r['account_number']
        for r in all_records
        if r['account_number']
    )


    conn.close()


    return render_template(

        "dashboard.html",

        sites=sites,

        active_site=active_site,

        results=all_records,

        total_records=len(all_records),

        username=session.get("username"),

        module=module,

        filters={},


        ip_counts=ip_counts,

        acct_counts=acct_counts

    )

@app.route('/add_record', methods=['POST'])
@login_required
def add_record():
    site_id = request.form.get('site_id', type=int)
    fa_name = request.form.get('fa_name', '').strip()
    processed_by = request.form.get('processed_by', '').strip()
    if not fa_name or not processed_by:
        flash("Kailangan ang Processed by at FA name.", "error")
        return redirect(url_for('dashboard', site_id=site_id))

    conn = db.get_conn()
    conn.execute(
        '''INSERT INTO record (site_id, processed_by, created_at, indication, fa_name, ip_address, game,
           username_field, account_name, account_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (site_id, processed_by, str(datetime.now(timezone.utc).replace(tzinfo=None)), request.form.get('indication', 'PLAYER'), fa_name,
         request.form.get('ip_address', '').strip(), request.form.get('game', '').strip(),
         request.form.get('username_field', '').strip(), request.form.get('account_name', '').strip(),
         request.form.get('account_number', '').strip())
    )
    conn.commit()
    conn.close()
    flash("Naidagdag ang record.", "success")
    return redirect(url_for('dashboard', site_id=site_id))


@app.route('/delete_record/<int:record_id>', methods=['POST'])
@login_required
def delete_record(record_id):

    conn = db.get_conn()

    row = conn.execute(
        'SELECT * FROM record WHERE id = ?',
        (record_id,)
    ).fetchone()


    if row:

        conn.execute(
            '''
            INSERT INTO audit_logs
            (
                username,
                action,
                target,
                details,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
            ''',
            (
                session.get('username'),
                'DELETE',
                'record',
                f"Deleted record ID {record_id}, FA: {row['fa_name']}",
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
        )


    conn.execute(
        'DELETE FROM record WHERE id = ?',
        (record_id,)
    )

    conn.commit()
    conn.close()

    flash("Na-delete ang record.", "success")

    return redirect(url_for('dashboard'))


@app.route('/manage_sites')
@login_required
def manage_sites():
    conn = db.get_conn()
    sites = conn.execute('SELECT * FROM site ORDER BY name').fetchall()
    counts = {}
    for s in sites:
        c = conn.execute('SELECT COUNT(*) AS c FROM record WHERE site_id = ?', (s['id'],)).fetchone()['c']
        counts[s['id']] = c
    conn.close()
    return render_template('manage_sites.html', sites=sites, counts=counts, username=session.get('username'))


@app.route('/add_site', methods=['POST'])
@login_required
def add_site():
    name = request.form.get('name', '').strip().upper()
    conn = db.get_conn()
    if not name:
        flash("Kailangan ng pangalan ng site.", "error")
    elif conn.execute('SELECT 1 FROM site WHERE name = ?', (name,)).fetchone():
        flash("Meron nang site na ganyan.", "error")
    else:
        conn.execute('INSERT INTO site (name) VALUES (?)', (name,))
        conn.commit()
        flash(f'Naidagdag ang site "{name}".', "success")
    conn.close()
    return redirect(url_for('manage_sites'))


@app.route('/delete_site/<int:site_id>', methods=['POST'])
@login_required
def delete_site(site_id):
    confirm_name = request.form.get('confirm_name', '').strip()
    conn = db.get_conn()
    site = conn.execute('SELECT * FROM site WHERE id = ?', (site_id,)).fetchone()
    if not site:
        flash("Site not found.", "error")
        conn.close()
        return redirect(url_for('manage_sites'))
    if confirm_name != site['name']:
        flash("Hindi tugma ang na-type na pangalan. Hindi natanggal ang site.", "error")
        conn.close()
        return redirect(url_for('manage_sites'))

    conn.execute('DELETE FROM record WHERE site_id = ?', (site_id,))
    conn.execute('DELETE FROM site WHERE id = ?', (site_id,))
    conn.commit()
    conn.close()
    flash(f'Natanggal ang site "{confirm_name}" at lahat ng records nito.', "success")
    return redirect(url_for('manage_sites'))


@app.route('/manage_staff')
@roles_required("ADMIN", "OM", "AOM")
def manage_staff():
    conn = db.get_conn()
    staff = conn.execute('SELECT * FROM user ORDER BY username').fetchall()
    conn.close()
    return render_template('manage_staff.html', staff=staff, username=session.get('username'))


@app.route('/add_staff', methods=['POST'])
@roles_required("ADMIN", "OM", "AOM")
def add_staff():

    username = request.form.get('new_username', '').strip()
    password = request.form.get('new_password', '')
    role = request.form.get('role', 'STAFF')

    conn = db.get_conn()

    if not username or not password:
        flash("Kailangan ng username at password.", "error")

    elif conn.execute(
        'SELECT 1 FROM user WHERE username = ?',
        (username,)
    ).fetchone():

        flash("Meron nang staff na ganyan ang username.", "error")

    else:

        conn.execute(
            '''
            INSERT INTO user
            (username, password_hash, role, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (
                username,
                generate_password_hash(password),
                role,
                'ACTIVE',
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
        )

        conn.commit()

        flash(
            f'Naidagdag ang staff account na "{username}".',
            "success"
        )

    conn.close()

    return redirect(url_for('manage_staff'))


@app.route('/delete_staff/<int:user_id>', methods=['POST'])
@roles_required("ADMIN", "OM", "AOM")
def delete_staff(user_id):
    if user_id == session.get('user_id'):
        flash("Hindi mo puwedeng tanggalin ang sarili mong account.", "error")
        return redirect(url_for('manage_staff'))
    
    conn = db.get_conn()
    conn.execute('DELETE FROM user WHERE id = ?', ('user_id',))
    conn.commit()
    conn.close()

    flash("Natanggal ang staff account.", "success")
    return redirect(url_for('manage_staff'))


# ==========================
# IMPORT KPI EXCEL
# ==========================

@app.route('/import_kpi', methods=['POST'])
@login_required
def import_kpi():

    file = request.files.get('excel_file')

    if not file:
        flash("Walang napiling Excel file.", "error")
        return redirect(url_for('dashboard', module='AGENT'))

    df = pd.read_excel(file)

    conn = db.get_conn()

    conn.execute("DELETE FROM kpi_data")

    for _, row in df.iterrows():

        conn.execute("""
            INSERT INTO kpi_data
            (
                AGENT,
                DEPOSIT,
                WITHDRAWAL,
                NET_DEPOSIT,
                PLAYER_COUNT,
                VTO,
                WINLOSS,
                COMMS,
                "COMMS%",
                OVER_ALL
            )
            VALUES (?,?,?,?,?,?,?,?,?,?)
        """,
        (
            str(row["AGENT"]),
            str(row["DEPOSIT"]),
            str(row["WITHDRAWAL"]),
            str(row["NET_DEPOSIT"]),
            str(row["PLAYER_COUNT"]),
            float(row["VTO"]),
            str(row["WINLOSS"]),
            str(row["COMMS"]),
            str(row["COMMS%"]),
            str(row["OVER_ALL"])
        ))

    conn.commit()
    conn.close()

    flash("KPI Excel Imported Successfully!", "success")

    return redirect(url_for('dashboard', module='AGENT'))



def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper


def audit_access_required(f):

    @wraps(f)
    def wrapper(*args, **kwargs):

        if 'user_id' not in session:
            return redirect(url_for('login'))

        if session.get('role') not in [
            'ADMIN',
            'OM',
            'AOM',
            'TL'
        ]:
            flash("Wala kang permission para makita ang Audit Logs.", "error")
            return redirect(url_for('dashboard'))

        return f(*args, **kwargs)

    return wrapper


db.init_db()
db.seed_defaults(generate_password_hash)

@app.route('/audit_logs')
@login_required
def audit_logs():

    search = request.args.get('search', '').strip()

    conn = db.get_conn()


    if search:

        logs = conn.execute(
            '''
            SELECT *
            FROM audit_logs

            WHERE username LIKE ?
            OR action LIKE ?
            OR target LIKE ?
            OR details LIKE ?
            OR created_at LIKE ?

            ORDER BY created_at DESC
            ''',
            (
                f'%{search}%',
                f'%{search}%',
                f'%{search}%',
                f'%{search}%',
                f'%{search}%'
            )
        ).fetchall()


    else:

        logs = conn.execute(
            '''
            SELECT *
            FROM audit_logs
            ORDER BY created_at DESC
            '''
        ).fetchall()



    conn.close()


    return render_template(
        'auditlog.html',
        logs=logs,
        username=session.get('username'),
        search=search
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)