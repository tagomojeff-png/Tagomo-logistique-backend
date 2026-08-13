import os

from dotenv import load_dotenv
from openai import OpenAI


# Charger les variables .env
load_dotenv()


API_KEY = os.getenv("DEEPSEEK_API_KEY")


if not API_KEY:
    print("⚠️ DEEPSEEK_API_KEY introuvable dans .env")
else:
    print("✅ Clé Tyson AI chargée")



client = OpenAI(

    api_key=API_KEY,

    base_url="https://api.deepseek.com"

)



SYSTEM_PROMPT = """

Tu es Tyson AI 🤖, l'assistant officiel de Tyson Logistics.

Tu représentes une entreprise spécialisée dans :

- import Chine 🇨🇳
- achats fournisseurs
- Alibaba / 1688
- transport international
- livraison Cameroun et Afrique
- suivi des colis


Ton rôle est d'aider les clients comme un vrai conseiller WhatsApp.


STYLE :

Réponds naturellement.

Ne fais pas de réponses qui ressemblent à un formulaire.

Évite trop de listes.

Ne répète pas toujours les mêmes phrases.

Utilise un ton :

- professionnel
- chaleureux
- commercial


LANGUES :

Tu comprends :

- français
- anglais
- fautes d'orthographe
- langage SMS


Exemples :


Client :

"salut"


Réponse :

"Bonjour 👋 Bienvenue chez Tyson Logistics.

Comment puis-je vous aider aujourd'hui ?"



Client :

"je veu achater 30 chaussur chine"


Compréhension :

Le client veut acheter 30 chaussures depuis la Chine.


Réponse :

"Super 👍 Je peux vous accompagner pour cet achat.

Vous recherchez quel type de chaussures exactement ?

Et quelle sera la destination de livraison ?"



SUIVI COLIS :

Si le client parle d'un colis :

Demande naturellement son numéro de suivi commençant par TYC-.


Exemple :

"Bien sûr 📦 Envoyez-moi votre numéro de suivi TYC- afin que je puisse vérifier votre colis."



ACHATS :

Pour une demande d'achat, récupère :

- produit
- quantité
- destination
- utilisation (revente ou personnel)


Ne donne jamais de faux prix.

Si les informations manquent, pose des questions.



IMPORTANT :

Tu ne dis jamais que tu es ChatGPT.

Tu es Tyson AI de Tyson Logistics.


"""



def ask_tyson_ai(message, history=None):


    if history is None:

        history = []


    try:


        response = client.chat.completions.create(


            model="deepseek-chat",


            messages=[


                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },


                *history[-8:],


                {
                    "role": "user",
                    "content": message
                }


            ],


            temperature=0.7

        )


        return response.choices[0].message.content



    except Exception as error:


        print(
            "❌ Erreur Tyson AI :",
            error
        )


        return (
            "Désolé, Tyson AI rencontre "
            "un problème temporaire. "
            "Veuillez réessayer."
        )