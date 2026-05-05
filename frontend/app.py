import streamlit as st
import requests
from api_client import signup, login, get_tasks, create_task, update_task, delete_task

st.set_page_config(page_title="📝 Todo App", page_icon="✅", layout="centered")

# ── Khởi tạo session state ────────────────────────────────────────
if "user" not in st.session_state:
    st.session_state.user = None  # {"email", "uid", "idToken"}

if "show_signup" not in st.session_state:
    st.session_state.show_signup = False


# ── Helper ────────────────────────────────────────────────────────

def load_tasks():
    try:
        return get_tasks(st.session_state.user["idToken"])
    except Exception as e:
        st.error(f"Không tải được danh sách task: {e}")
        return []


# ── Form đăng nhập ────────────────────────────────────────────────

def show_login_form():
    st.subheader("🔐 Đăng nhập")

    email    = st.text_input("Email", key="login_email")
    password = st.text_input("Mật khẩu", type="password", key="login_password")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Đăng nhập", use_container_width=True, type="primary"):
            if not email or not password:
                st.warning("Vui lòng nhập đầy đủ email và mật khẩu.")
            else:
                try:
                    user = login(email, password)
                    st.session_state.user = user
                    st.success("Đăng nhập thành công!")
                    st.rerun()
                except requests.HTTPError:
                    st.error("Sai email hoặc mật khẩu.")
                except Exception as e:
                    st.error(f"Lỗi kết nối backend: {e}")

    with col2:
        if st.button("Tạo tài khoản mới", use_container_width=True):
            st.session_state.show_signup = True
            st.rerun()


# ── Form đăng ký ─────────────────────────────────────────────────

def show_signup_form():
    st.subheader("📋 Đăng ký tài khoản")

    email    = st.text_input("Email", key="signup_email")
    password = st.text_input("Mật khẩu (ít nhất 6 ký tự)", type="password", key="signup_password")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Tạo tài khoản", use_container_width=True, type="primary"):
            if not email or not password:
                st.warning("Vui lòng nhập đầy đủ thông tin.")
            elif len(password) < 6:
                st.error("Mật khẩu phải có ít nhất 6 ký tự.")
            else:
                try:
                    signup(email, password)
                    st.success("Tạo tài khoản thành công! Hãy đăng nhập.")
                    st.session_state.show_signup = False
                    st.rerun()
                except requests.HTTPError as e:
                    st.error(f"Đăng ký thất bại: {e}")
                except Exception as e:
                    st.error(f"Lỗi: {e}")

    with col2:
        if st.button("← Quay lại đăng nhập", use_container_width=True):
            st.session_state.show_signup = False
            st.rerun()


# ── Giao diện chính ───────────────────────────────────────────────

def show_main_app():
    user = st.session_state.user

    # Thanh thông tin user + nút đăng xuất
    col1, col2 = st.columns([4, 1])
    with col1:
        st.success(f"👤 Đang đăng nhập: **{user['email']}**")
    with col2:
        if st.button("Đăng xuất", use_container_width=True):
            st.session_state.user = None
            st.rerun()

    st.divider()

    # ── Form thêm task mới ────────────────────────────────────────
    st.subheader("➕ Thêm task mới")

    with st.form("add_task_form", clear_on_submit=True):
        title       = st.text_input("Tên công việc *", placeholder="Ví dụ: Ôn tập môn Tư duy tính toán")
        description = st.text_area("Mô tả (tuỳ chọn)", placeholder="Ghi thêm chi tiết nếu cần...")
        submitted   = st.form_submit_button("➕ Thêm task", use_container_width=True)

    if submitted:
        if not title.strip():
            st.error("Tên công việc không được để trống!")
        else:
            try:
                create_task(user["idToken"], title.strip(), description.strip())
                st.success(f"✅ Đã thêm: **{title.strip()}**")
                st.rerun()
            except Exception as e:
                st.error(f"Lỗi khi thêm task: {e}")

    st.divider()

    # ── Danh sách tasks ───────────────────────────────────────────
    st.subheader("📋 Danh sách công việc")

    tasks = load_tasks()

    if not tasks:
        st.info("Chưa có công việc nào. Hãy thêm task đầu tiên ở trên!")
        return

    # Thống kê nhanh
    total = len(tasks)
    done  = sum(1 for t in tasks if t["completed"])
    st.caption(f"**Tổng:** {total} &nbsp;|&nbsp; ✅ Hoàn thành: {done} &nbsp;|&nbsp; 🔲 Còn lại: {total - done}")

    # Hiển thị từng task
    for task in tasks:
        task_id = task["id"]
        is_done = task["completed"]

        with st.container(border=True):
            col_check, col_info, col_del = st.columns([0.08, 3.5, 0.4])

            with col_check:
                new_status = st.checkbox(
                    label="done",
                    value=is_done,
                    key=f"chk_{task_id}",
                    label_visibility="collapsed",
                )
                # Nếu user bấm toggle → gọi API cập nhật
                if new_status != is_done:
                    try:
                        update_task(user["idToken"], task_id, new_status)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Lỗi cập nhật: {e}")

            with col_info:
                if is_done:
                    st.markdown(f"~~**{task['title']}**~~")
                else:
                    st.markdown(f"**{task['title']}**")

                if task.get("description"):
                    st.caption(task["description"])

            with col_del:
                if st.button("🗑️", key=f"del_{task_id}", help="Xoá task này"):
                    try:
                        delete_task(user["idToken"], task_id)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Lỗi xoá task: {e}")


# ── Entry point ───────────────────────────────────────────────────

st.title("📝 Todo App")

if st.session_state.user:
    show_main_app()
else:
    if st.session_state.show_signup:
        show_signup_form()
    else:
        show_login_form()
