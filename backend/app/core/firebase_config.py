import streamlit as st
import firebase_admin
import pyrebase
from firebase_admin import credentials, firestore


def get_pyrebase_auth():
    """Khởi tạo Pyrebase để xử lý Email/Password login"""
    firebase_cfg = dict(st.secrets["firebase_client"])
    firebase_app = pyrebase.initialize_app(firebase_cfg)
    return firebase_app.auth()


def init_firebase_admin():
    """Khởi tạo Firebase Admin SDK (chỉ khởi tạo 1 lần duy nhất)"""
    if not firebase_admin._apps:
        cred_dict = dict(st.secrets["firebase_admin"])
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)


def get_firestore():
    """Lấy Firestore client"""
    init_firebase_admin()
    return firestore.client()
