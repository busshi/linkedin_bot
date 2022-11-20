import os

LINKEDIN_URL = 'https://www.linkedin.com'
LINKEDIN_NETWORK_URL = f'{LINKEDIN_URL}/mynetwork'
LINKEDIN_MESSAGES_URL = f'{LINKEDIN_URL}/messaging'

TELEGRAM_URL = 'https://api.telegram.org/'

COLORS = {
    'red': '\033[31m',
    'green': '\033[32m',
    'orange': '\033[33m',
    'clear': '\033[0m'
}    

CONTACTS_FILE = f'{os.getcwd()}/data/contacts.txt'
COOKIES_FILE = f'{os.getcwd()}/data/.cookies'

ARGS_LIST = ['--headless', '--telegram']

WELCOME_MESSAGE = ['👋', 'Bonjour,', 'Bienvenue dans mon réseau.', 'Si vous voulez en savoir plus sur moi, vous pouvez demander à mon bot quelques informations basiques à l\'aide des commandes suivantes :', '- profile : pour en savoir un peu plus sur moi', '- techno : pour connaître mes technologies préférées', '- dispo : pour connaître mes disponibilités', '- contact : pour me parler directement au lieu de communiquer avec un bot', '- unmute : pour réactiver le bot après une demande de contact']

ACTIONS = {
    'dispo': ['Je suis actuellement disponible les soirs et weekends pour collaborer avec vous.', 'N\'hésitez pas à me contacter pour en discuter, je suis assez flexible sur l\'emploi du temps'],
    'techno': ['Mes compétences principales concernent les frameworks suivants :', '• Frontend: React, NextJS', '• Backend: ExpressJS, NestJS, Python', '• Devops: Déploiement en ligne avec Google Cloud Platform, Cloudflare, OVH', '• SEO: Optimisation dans les moteurs de recherche', 'J\'ai bien sûr d\'autres cordes à mon arc. Je développe de nombreux projets personnels autour du Web, de la domotique et de la cyber-sécurité... Demandes-en moi plus si cela t\'intéresse'],
    'profile': ['Je suis plutôt cool et déter. J\'aime ce que je fais et je suis épanoui dans mon travail ce qui me permet d\'être plus productif.', 'Autodidacte, je me forme en permanence pour rester à la pointe des dernières technologies.', 'Je travaille essentiellement dans le web en tant que développeur fullstack mais je m\'adapte très facilement.', '😎', 'Jetez un oeil à mon profil sur Malt : https://www.malt.fr/profile/alexandredubar'],
    'contact': ['J\'ai transmis votre demande de communiquer avec mon créateur. Il vous répondra en personne dès que possible...', 'Je resterai muet en attendant... 🫢', 'Unmute pour me réactiver'],
    'unmute': ['👋', 'Rappel des commandes disponibles :', '- profile : pour en savoir un peu plus sur moi', '- techno : pour connaître les technologies que je maîtrise', '- dispo : pour connaître mes disponibilités', '- contact : pour me parler directement...', '- unmute : pour réactiver le bot']
}    

DOM_VARIABLES = {
    'login_user': 'session_key',
    'login_password': 'session_password',
    'human_check': "//*[text()='Procédons à une petite vérification de sécurité']",
    'tfa_pin': 'input__phone_verification_pin',
    'reduce_messaging': "//button[contains(@class, 'artdeco-button--muted artdeco-button--1 artdeco-button--tertiary')]",
    'new_connexion': 'invitation-card__action-btn',
    'connexion_request': 'artdeco-button--secondary',
    'accept_connexion': "//button[contains(@class, 'artdeco-button artdeco-button--2 artdeco-button--secondary ember-view invitation-card__action-btn')]",
    'write_message': "//button[contains(@class, 'invitation-inline-confirmation-card__message-cta')]",
    'search_conversations': 'search-conversations',
    'search_message_contact': 'msg-conversation-card__content--selectable',
    'unread_message': 'msg-conversation-card__message-snippet--unread',
    'message_input_form': 'div.msg-form__contenteditable',
}
