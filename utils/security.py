# -*- coding: utf-8 -*-
import hashlib
import re

def validar_email(email):
    """Validar formato de email"""
    patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron_email, email) is not None

def validar_contraseña(contraseña):
    """Validar fortaleza de contraseña"""
    return (
        len(contraseña) >= 8 and  # Mínimo 8 caracteres
        any(c.isupper() for c in contraseña) and  # Al menos una mayúscula
        any(c.islower() for c in contraseña) and  # Al menos una minúscula
        any(c.isdigit() for c in contraseña)      # Al menos un número
    )

def hash_contraseña(contraseña):
    """Generar hash SHA-256 de contraseña"""
    return hashlib.sha256(contraseña.encode()).hexdigest()