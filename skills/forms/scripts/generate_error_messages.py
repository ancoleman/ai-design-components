#!/usr/bin/env python3
"""
Generate i18n Error Message Files

Creates error message files for multiple languages from templates.

Usage:
    python generate_error_messages.py --lang en --output errors-en.json
    python generate_error_messages.py --lang es --output errors-es.json
"""

import argparse
import json
from pathlib import Path

# Error message templates by language
ERROR_TEMPLATES = {
    'en': {
        'required': '{field} is required',
        'email': 'Please enter a valid email address',
        'minLength': '{field} must be at least {min} characters',
        'maxLength': '{field} must be less than {max} characters',
        'min': '{field} must be at least {min}',
        'max': '{field} must be at most {max}',
        'pattern': '{field} format is invalid',
        'url': 'Please enter a valid URL',
        'date': 'Please enter a valid date',
        'password': {
            'minLength': 'Password must be at least 8 characters',
            'uppercase': 'Password must contain at least one uppercase letter',
            'lowercase': 'Password must contain at least one lowercase letter',
            'number': 'Password must contain at least one number',
            'special': 'Password must contain at least one special character'
        },
        'confirmPassword': 'Passwords do not match',
        'username': {
            'taken': 'Username is already taken',
            'invalid': 'Username can only contain letters, numbers, and underscores',
            'minLength': 'Username must be at least 3 characters'
        },
        'phone': 'Please enter a valid phone number',
        'creditCard': 'Please enter a valid credit card number',
        'integer': '{field} must be a whole number',
        'positive': '{field} must be a positive number',
        'future': '{field} must be in the future',
        'past': '{field} must be in the past'
    },
    'es': {
        'required': '{field} es obligatorio',
        'email': 'Por favor ingrese un correo electrónico válido',
        'minLength': '{field} debe tener al menos {min} caracteres',
        'maxLength': '{field} debe tener menos de {max} caracteres',
        'min': '{field} debe ser al menos {min}',
        'max': '{field} debe ser como máximo {max}',
        'pattern': 'El formato de {field} no es válido',
        'url': 'Por favor ingrese una URL válida',
        'date': 'Por favor ingrese una fecha válida',
        'password': {
            'minLength': 'La contraseña debe tener al menos 8 caracteres',
            'uppercase': 'La contraseña debe contener al menos una letra mayúscula',
            'lowercase': 'La contraseña debe contener al menos una letra minúscula',
            'number': 'La contraseña debe contener al menos un número',
            'special': 'La contraseña debe contener al menos un carácter especial'
        },
        'confirmPassword': 'Las contraseñas no coinciden',
        'username': {
            'taken': 'El nombre de usuario ya está en uso',
            'invalid': 'El nombre de usuario solo puede contener letras, números y guiones bajos',
            'minLength': 'El nombre de usuario debe tener al menos 3 caracteres'
        },
        'phone': 'Por favor ingrese un número de teléfono válido',
        'creditCard': 'Por favor ingrese un número de tarjeta de crédito válido',
        'integer': '{field} debe ser un número entero',
        'positive': '{field} debe ser un número positivo',
        'future': '{field} debe ser una fecha futura',
        'past': '{field} debe ser una fecha pasada'
    },
    'fr': {
        'required': '{field} est requis',
        'email': 'Veuillez saisir une adresse e-mail valide',
        'minLength': '{field} doit contenir au moins {min} caractères',
        'maxLength': '{field} doit contenir moins de {max} caractères',
        'min': '{field} doit être au moins {min}',
        'max': '{field} doit être au plus {max}',
        'pattern': 'Le format de {field} n\'est pas valide',
        'url': 'Veuillez saisir une URL valide',
        'date': 'Veuillez saisir une date valide',
        'password': {
            'minLength': 'Le mot de passe doit contenir au moins 8 caractères',
            'uppercase': 'Le mot de passe doit contenir au moins une lettre majuscule',
            'lowercase': 'Le mot de passe doit contenir au moins une lettre minuscule',
            'number': 'Le mot de passe doit contenir au moins un chiffre',
            'special': 'Le mot de passe doit contenir au moins un caractère spécial'
        },
        'confirmPassword': 'Les mots de passe ne correspondent pas',
        'username': {
            'taken': 'Ce nom d\'utilisateur est déjà pris',
            'invalid': 'Le nom d\'utilisateur ne peut contenir que des lettres, chiffres et traits de soulignement',
            'minLength': 'Le nom d\'utilisateur doit contenir au moins 3 caractères'
        },
        'phone': 'Veuillez saisir un numéro de téléphone valide',
        'creditCard': 'Veuillez saisir un numéro de carte de crédit valide',
        'integer': '{field} doit être un nombre entier',
        'positive': '{field} doit être un nombre positif',
        'future': '{field} doit être une date future',
        'past': '{field} doit être une date passée'
    },
    'de': {
        'required': '{field} ist erforderlich',
        'email': 'Bitte geben Sie eine gültige E-Mail-Adresse ein',
        'minLength': '{field} muss mindestens {min} Zeichen lang sein',
        'maxLength': '{field} muss weniger als {max} Zeichen lang sein',
        'min': '{field} muss mindestens {min} sein',
        'max': '{field} darf höchstens {max} sein',
        'pattern': 'Das Format von {field} ist ungültig',
        'url': 'Bitte geben Sie eine gültige URL ein',
        'date': 'Bitte geben Sie ein gültiges Datum ein',
        'password': {
            'minLength': 'Das Passwort muss mindestens 8 Zeichen lang sein',
            'uppercase': 'Das Passwort muss mindestens einen Großbuchstaben enthalten',
            'lowercase': 'Das Passwort muss mindestens einen Kleinbuchstaben enthalten',
            'number': 'Das Passwort muss mindestens eine Zahl enthalten',
            'special': 'Das Passwort muss mindestens ein Sonderzeichen enthalten'
        },
        'confirmPassword': 'Die Passwörter stimmen nicht überein',
        'username': {
            'taken': 'Dieser Benutzername ist bereits vergeben',
            'invalid': 'Der Benutzername darf nur Buchstaben, Zahlen und Unterstriche enthalten',
            'minLength': 'Der Benutzername muss mindestens 3 Zeichen lang sein'
        },
        'phone': 'Bitte geben Sie eine gültige Telefonnummer ein',
        'creditCard': 'Bitte geben Sie eine gültige Kreditkartennummer ein',
        'integer': '{field} muss eine ganze Zahl sein',
        'positive': '{field} muss eine positive Zahl sein',
        'future': '{field} muss in der Zukunft liegen',
        'past': '{field} muss in der Vergangenheit liegen'
    }
}

def main():
    parser = argparse.ArgumentParser(description='Generate error message files for i18n')
    parser.add_argument('--lang', choices=list(ERROR_TEMPLATES.keys()),
                       required=True, help='Language code')
    parser.add_argument('--output', type=str, help='Output JSON file')

    args = parser.parse_args()

    messages = ERROR_TEMPLATES[args.lang]
    output = json.dumps(messages, indent=2, ensure_ascii=False)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(output, encoding='utf-8')
        print(f"✅ Error messages ({args.lang}) saved to {output_path}")
    else:
        print(f"\nError Messages ({args.lang.upper()}):")
        print(output)

if __name__ == "__main__":
    main()
