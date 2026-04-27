import re
import json
from typing import Dict, List, Tuple
import random

class MedicalAI:
    def __init__(self):
        # Try to load trained model first
        try:
            with open('trained_model.json', 'r', encoding='utf-8') as f:
                trained_data = json.load(f)
                self.knowledge_base = trained_data.get('knowledge_base', {})
                self.symptom_keywords = trained_data.get('symptom_keywords', {})
                self.condition_patterns = trained_data.get('condition_patterns', {})
                print(f"✅ Loaded trained AI with {trained_data.get('training_examples_count', 0)} examples")
        except FileNotFoundError:
            # Fall back to default knowledge
            self.knowledge_base = self._load_knowledge_base()
            self.symptom_keywords = self._load_symptom_keywords()
            self.condition_patterns = self._load_condition_patterns()
            print("📚 Using default medical knowledge base")
        
    def _load_knowledge_base(self) -> Dict:
        """Load comprehensive medical knowledge base"""
        return {
            "headache": {
                "symptoms": ["headache", "migraine", "head pain", "throbbing head"],
                "causes": ["stress", "dehydration", "lack of sleep", "eye strain", "sinus issues"],
                "remedies": [
                    "Rest in a quiet, dark room",
                    "Stay hydrated with water",
                    "Apply cold compress to forehead",
                    "Take over-the-counter pain relievers (acetaminophen, ibuprofen)",
                    "Practice relaxation techniques"
                ],
                "warning_signs": [
                    "Severe headache that comes on suddenly",
                    "Headache with fever, stiff neck, confusion",
                    "Headache after head injury",
                    "Worst headache of your life"
                ],
                "disclaimer": "This is not a substitute for professional medical advice."
            },
            "fever": {
                "symptoms": ["fever", "high temperature", "chills", "sweating"],
                "causes": ["infection", "viral illness", "bacterial infection", "inflammation"],
                "remedies": [
                    "Get plenty of rest",
                    "Stay hydrated with fluids",
                    "Take lukewarm baths",
                    "Wear light clothing",
                    "Monitor temperature regularly"
                ],
                "warning_signs": [
                    "Fever above 103°F (39.4°C)",
                    "Fever lasting more than 3 days",
                    "Fever with severe headache, stiff neck",
                    "Fever with difficulty breathing"
                ],
                "disclaimer": "Seek medical attention for persistent or high fevers."
            },
            "cough": {
                "symptoms": ["cough", "coughing", "chesty cough", "dry cough"],
                "causes": ["cold", "flu", "allergies", "asthma", "acid reflux"],
                "remedies": [
                    "Stay hydrated with warm fluids",
                    "Use honey to soothe throat",
                    "Try steam inhalation",
                    "Use a humidifier",
                    "Avoid irritants like smoke"
                ],
                "warning_signs": [
                    "Cough lasting more than 2 weeks",
                    "Coughing up blood",
                    "Cough with shortness of breath",
                    "Cough with chest pain"
                ],
                "disclaimer": "Persistent coughs require medical evaluation."
            },
            "stomach_pain": {
                "symptoms": ["stomach pain", "abdominal pain", "belly pain", "stomach ache"],
                "causes": ["indigestion", "food poisoning", "gas", "ulcer", "appendicitis"],
                "remedies": [
                    "Rest and avoid solid foods temporarily",
                    "Stay hydrated with clear fluids",
                    "Try BRAT diet (banana, rice, applesauce, toast)",
                    "Avoid spicy and fatty foods",
                    "Apply gentle heat to abdomen"
                ],
                "warning_signs": [
                    "Severe abdominal pain",
                    "Pain with fever",
                    "Pain with vomiting blood",
                    "Pain in lower right abdomen",
                    "Pain lasting more than 24 hours"
                ],
                "disclaimer": "Severe abdominal pain requires immediate medical attention."
            },
            "fatigue": {
                "symptoms": ["fatigue", "tired", "exhausted", "weak", "no energy", "sleepy"],
                "causes": ["lack of sleep", "stress", "poor nutrition", "anemia", "thyroid issues"],
                "remedies": [
                    "Ensure 7-9 hours of quality sleep",
                    "Maintain regular sleep schedule",
                    "Eat balanced diet rich in iron and vitamins",
                    "Exercise regularly",
                    "Manage stress through relaxation"
                ],
                "warning_signs": [
                    "Fatigue lasting more than 2 weeks",
                    "Fatigue with unexplained weight loss",
                    "Fatigue with fever or pain",
                    "Extreme fatigue interfering with daily life"
                ],
                "disclaimer": "Chronic fatigue may indicate underlying medical conditions."
            },
            "chest_pain": {
                "symptoms": ["chest pain", "chest tightness", "chest discomfort", "heart pain"],
                "causes": ["heart attack", "angina", "heartburn", "anxiety", "muscle strain"],
                "remedies": [
                    "Call emergency services immediately",
                    "Chew aspirin if available (if not allergic)",
                    "Sit down and rest",
                    "Loosen tight clothing",
                    "Stay calm"
                ],
                "warning_signs": [
                    "Severe chest pain or pressure",
                    "Pain spreading to arm, jaw, or back",
                    "Chest pain with shortness of breath",
                    "Chest pain with sweating or nausea"
                ],
                "disclaimer": "Chest pain can be life-threatening - seek immediate emergency care."
            },
            "breathing_difficulty": {
                "symptoms": ["shortness of breath", "difficulty breathing", "wheezing", "can't breathe"],
                "causes": ["asthma", "copd", "pneumonia", "anxiety", "heart failure"],
                "remedies": [
                    "Sit upright and lean forward",
                    "Use prescribed inhaler if available",
                    "Practice breathing exercises",
                    "Remove triggers (allergens, smoke)",
                    "Stay calm"
                ],
                "warning_signs": [
                    "Severe shortness of breath",
                    "Blue lips or face",
                    "Chest pain with breathing difficulty",
                    "Confusion or extreme drowsiness"
                ],
                "disclaimer": "Breathing difficulties require immediate medical attention."
            },
            "diabetes": {
                "symptoms": ["diabetes", "high blood sugar", "thirsty", "frequent urination"],
                "causes": ["insulin resistance", "autoimmune", "genetics", "lifestyle"],
                "remedies": [
                    "Monitor blood sugar regularly",
                    "Take medications as prescribed",
                    "Follow diabetic diet",
                    "Exercise regularly",
                    "Maintain healthy weight"
                ],
                "warning_signs": [
                    "Very high blood sugar readings",
                    "Fruity-smelling breath",
                    "Extreme thirst and urination",
                    "Confusion or loss of consciousness"
                ],
                "disclaimer": "Diabetes requires ongoing medical management."
            },
            "hypertension": {
                "symptoms": ["high blood pressure", "hypertension", "elevated blood pressure"],
                "causes": ["genetics", "obesity", "stress", "high sodium intake", "lack of exercise"],
                "remedies": [
                    "Reduce sodium intake",
                    "Exercise regularly",
                    "Maintain healthy weight",
                    "Limit alcohol",
                    "Take blood pressure medications"
                ],
                "warning_signs": [
                    "Blood pressure above 180/120",
                    "Severe headache",
                    "Chest pain or difficulty breathing",
                    "Vision changes or confusion"
                ],
                "disclaimer": "High blood pressure often has no symptoms but can be dangerous."
            },
            "arthritis": {
                "symptoms": ["arthritis", "joint pain", "stiff joints", "joint inflammation"],
                "causes": ["autoimmune", "wear and tear", "injury", "genetics", "age"],
                "remedies": [
                    "Low-impact exercise",
                    "Apply heat or cold packs",
                    "Maintain healthy weight",
                    "Use assistive devices",
                    "Take anti-inflammatory medications"
                ],
                "warning_signs": [
                    "Severe joint pain",
                    "Joint swelling and redness",
                    "Fever with joint pain",
                    "Inability to move joint"
                ],
                "disclaimer": "Arthritis requires proper diagnosis and management."
            },
            "depression": {
                "symptoms": ["depression", "sad", "hopeless", "no motivation", "lost interest"],
                "causes": ["chemical imbalance", "genetics", "trauma", "stress", "medical conditions"],
                "remedies": [
                    "Seek professional counseling",
                    "Exercise regularly",
                    "Maintain social connections",
                    "Practice mindfulness and meditation",
                    "Consider antidepressant medication"
                ],
                "warning_signs": [
                    "Thoughts of self-harm",
                    "Extreme hopelessness",
                    "Inability to function daily",
                    "Withdrawal from all activities"
                ],
                "disclaimer": "Depression is a serious medical condition requiring professional help."
            },
            "anxiety": {
                "symptoms": ["anxiety", "worried", "panic", "nervous", "anxious"],
                "causes": ["stress", "genetics", "trauma", "medical conditions", "brain chemistry"],
                "remedies": [
                    "Practice deep breathing exercises",
                    "Exercise regularly",
                    "Limit caffeine and alcohol",
                    "Get adequate sleep",
                    "Consider therapy or counseling"
                ],
                "warning_signs": [
                    "Panic attacks",
                    "Anxiety interfering with daily life",
                    "Physical symptoms like chest pain",
                    "Avoidance of normal activities"
                ],
                "disclaimer": "Severe anxiety may require professional medical treatment."
            },
            "skin_rash": {
                "symptoms": ["skin rash", "rash", "itchy skin", "red spots", "skin irritation"],
                "causes": ["allergies", "infections", "autoimmune", "medications", "environment"],
                "remedies": [
                    "Apply cool compress",
                    "Use over-the-counter hydrocortisone cream",
                    "Take oatmeal baths",
                    "Avoid scratching",
                    "Use fragrance-free moisturizers"
                ],
                "warning_signs": [
                    "Rash spreading rapidly",
                    "Rash with fever",
                    "Blisters or open sores",
                    "Rash covering large body area"
                ],
                "disclaimer": "Persistent or severe rashes require medical evaluation."
            },
            "allergies": {
                "symptoms": ["allergies", "allergic reaction", "sneezing", "runny nose", "itchy eyes"],
                "causes": ["pollen", "dust", "pet dander", "food", "medications"],
                "remedies": [
                    "Avoid known allergens",
                    "Take antihistamines",
                    "Use nasal sprays",
                    "Keep windows closed during high pollen",
                    "Use air purifiers"
                ],
                "warning_signs": [
                    "Difficulty breathing",
                    "Swelling of face or throat",
                    "Hives covering large areas",
                    "Anaphylaxis symptoms"
                ],
                "disclaimer": "Severe allergic reactions require emergency medical care."
            },
            "insomnia": {
                "symptoms": ["insomnia", "can't sleep", "sleep problems", "trouble sleeping"],
                "causes": ["stress", "medical conditions", "medications", "poor sleep habits", "anxiety"],
                "remedies": [
                    "Maintain consistent sleep schedule",
                    "Create relaxing bedtime routine",
                    "Avoid screens before bed",
                    "Keep bedroom cool and dark",
                    "Avoid caffeine late in day"
                ],
                "warning_signs": [
                    "Sleep problems lasting weeks",
                    "Falling asleep during activities",
                    "Sleep problems affecting work",
                    "Dependence on sleep medications"
                ],
                "disclaimer": "Chronic insomnia may indicate underlying medical conditions."
            },
            "back_pain": {
                "symptoms": ["back pain", "backache", "lower back pain", "spine pain"],
                "causes": ["muscle strain", "herniated disc", "arthritis", "poor posture", "injury"],
                "remedies": [
                    "Apply ice or heat packs",
                    "Gentle stretching exercises",
                    "Maintain good posture",
                    "Use proper lifting techniques",
                    "Consider physical therapy"
                ],
                "warning_signs": [
                    "Pain radiating down legs",
                    "Numbness or weakness",
                    "Pain after injury",
                    "Pain with fever or chills"
                ],
                "disclaimer": "Severe or persistent back pain requires medical evaluation."
            },
            "eye_problems": {
                "symptoms": ["eye pain", "vision problems", "blurry vision", "red eyes"],
                "causes": ["eye strain", "infections", "injuries", "glaucoma", "cataracts"],
                "remedies": [
                    "Rest eyes regularly",
                    "Use artificial tears",
                    "Adjust screen brightness",
                    "Take breaks from screens",
                    "Wear sunglasses outdoors"
                ],
                "warning_signs": [
                    "Sudden vision loss",
                    "Severe eye pain",
                    "Flashes of light or floaters",
                    "Eye injury or trauma"
                ],
                "disclaimer": "Sudden vision changes require immediate medical attention."
            },
            "dizziness": {
                "symptoms": ["dizziness", "vertigo", "lightheaded", "off balance"],
                "causes": ["inner ear problems", "low blood pressure", "dehydration", "medications", "anxiety"],
                "remedies": [
                    "Sit or lie down immediately",
                    "Drink water",
                    "Avoid sudden movements",
                    "Focus on a fixed point",
                    "Get up slowly from sitting"
                ],
                "warning_signs": [
                    "Dizziness with chest pain",
                    "Fainting or loss of consciousness",
                    "Severe headache with dizziness",
                    "Difficulty speaking or walking"
                ],
                "disclaimer": "Persistent dizziness requires medical evaluation."
            },
            "nausea_vomiting": {
                "symptoms": ["nausea", "vomiting", "queasy", "throw up", "upset stomach"],
                "causes": ["food poisoning", "viral infection", "motion sickness", "pregnancy", "migraine"],
                "remedies": [
                    "Sip clear fluids slowly",
                    "Eat bland foods",
                    "Rest in upright position",
                    "Try ginger or peppermint",
                    "Avoid strong odors"
                ],
                "warning_signs": [
                    "Vomiting blood",
                    "Severe abdominal pain",
                    "Signs of dehydration",
                    "Vomiting lasting more than 24 hours"
                ],
                "disclaimer": "Persistent vomiting can lead to dehydration and requires medical care."
            },
            "leg_pain": {
                "symptoms": ["leg pain", "leg ache", "sore legs", "painful legs", "leg discomfort"],
                "causes": ["muscle strain", "overuse", "injury", "poor circulation", "nerve issues", "arthritis"],
                "remedies": [
                    "Rest and elevate legs",
                    "Apply ice or heat packs",
                    "Gentle stretching exercises",
                    "Massage the affected area",
                    "Take over-the-counter pain relievers"
                ],
                "warning_signs": [
                    "Severe or sudden leg pain",
                    "Pain with swelling or redness",
                    "Inability to bear weight",
                    "Pain after injury or trauma"
                ],
                "disclaimer": "Severe or persistent leg pain requires medical evaluation."
            },
            "hand_pain": {
                "symptoms": ["hand pain", "hand ache", "sore hands", "painful hands", "hand discomfort"],
                "causes": ["carpal tunnel", "arthritis", "overuse", "injury", "repetitive strain", "nerve compression"],
                "remedies": [
                    "Rest hands and wrists",
                    "Apply ice to reduce swelling",
                    "Do hand stretching exercises",
                    "Use ergonomic equipment",
                    "Take anti-inflammatory medications"
                ],
                "warning_signs": [
                    "Severe hand pain",
                    "Numbness or tingling",
                    "Loss of grip strength",
                    "Pain with swelling or deformity"
                ],
                "disclaimer": "Persistent hand pain may indicate underlying conditions requiring medical attention."
            }
        }
    
    def _load_symptom_keywords(self) -> Dict[str, List[str]]:
        """Load comprehensive symptom keyword mappings"""
        return {
            "headache": ["headache", "head", "migraine", "pain in head", "throbbing", "headache pain"],
            "fever": ["fever", "temperature", "hot", "chills", "sweating", "feverish", "high temp"],
            "cough": ["cough", "coughing", "chesty", "dry cough", "throat", "persistent cough"],
            "stomach": ["stomach", "abdomen", "belly", "tummy", "gut", "digestive", "stomach ache", "stomach pain", "abdominal pain", "belly ache", "tummy pain"],
            "pain": ["pain", "ache", "hurt", "sore", "discomfort", "uncomfortable", "painful"],
            "fatigue": ["tired", "fatigue", "exhausted", "weak", "no energy", "sleepy", "lethargic", "drained"],
            "nausea": ["nausea", "queasy", "sick", "vomit", "throw up", "upset stomach", "nauseous"],
            "chest": ["chest", "chest pain", "chest tightness", "heart", "cardiac", "chest discomfort"],
            "breathing": ["breathing", "breath", "shortness of breath", "wheezing", "can't breathe", "difficulty breathing", "respiratory"],
            "diabetes": ["diabetes", "blood sugar", "glucose", "thirsty", "frequent urination", "high blood sugar"],
            "blood_pressure": ["blood pressure", "hypertension", "high blood pressure", "elevated blood pressure", "bp"],
            "joint": ["joint", "joints", "arthritis", "joint pain", "stiff joints", "joint inflammation"],
            "mental_health": ["depression", "depressed", "sad", "hopeless", "anxiety", "anxious", "panic", "worried", "mental health"],
            "skin": ["skin", "rash", "itchy", "red spots", "skin irritation", "hives", "dermatitis"],
            "allergy": ["allergy", "allergies", "allergic", "sneezing", "runny nose", "itchy eyes", "hay fever"],
            "sleep": ["sleep", "insomnia", "can't sleep", "sleep problems", "trouble sleeping", "sleepless"],
            "back": ["back", "back pain", "backache", "lower back", "spine", "spinal"],
            "leg": ["leg", "legs", "leg pain", "leg ache", "sore legs", "painful legs", "thigh", "calf", "shin"],
            "hand": ["hand", "hands", "hand pain", "hand ache", "sore hands", "painful hands", "wrist", "fingers", "palm"],
            "eye": ["eye", "eyes", "vision", "blurry vision", "eye pain", "red eyes", "sight"],
            "dizziness": ["dizzy", "dizziness", "vertigo", "lightheaded", "off balance", "unsteady"],
            "vomiting": ["vomiting", "vomit", "throwing up", "emesis", "puking"]
        }
    
    def _load_condition_patterns(self) -> Dict[str, List[str]]:
        """Load comprehensive condition recognition patterns"""
        return {
            "emergency": [
                "chest pain", "difficulty breathing", "severe pain", "bleeding",
                "unconscious", "confusion", "stroke", "heart attack", "suicidal",
                "can't breathe", "severe bleeding", "loss of consciousness"
            ],
            "urgent": [
                "high fever", "persistent vomiting", "severe headache", "broken bone",
                "deep wound", "poisoning", "allergic reaction", "severe abdominal pain",
                "difficulty speaking", "vision loss", "numbness", "weakness"
            ],
            "general": [
                "cold", "flu", "headache", "stomach ache", "minor pain", "fatigue",
                "mild fever", "cough", "sore throat", "insomnia", "stress", "anxiety"
            ]
        }
    
    def _extract_symptoms(self, user_input: str) -> List[str]:
        """Extract symptoms from user input"""
        user_input = user_input.lower()
        found_symptoms = []
        
        for symptom, keywords in self.symptom_keywords.items():
            for keyword in keywords:
                if keyword in user_input:
                    found_symptoms.append(symptom)
                    break
        
        # Check for combined symptoms
        if 'stomach' in found_symptoms and 'pain' in found_symptoms:
            found_symptoms.append('stomach_pain')
        if 'chest' in found_symptoms and 'pain' in found_symptoms:
            found_symptoms.append('chest_pain')
        if 'breathing' in found_symptoms:
            found_symptoms.append('breathing_difficulty')
        if 'nausea' in found_symptoms or 'vomiting' in found_symptoms:
            found_symptoms.append('nausea_vomiting')
        if 'mental_health' in found_symptoms:
            if 'depression' in user_input or 'sad' in user_input or 'hopeless' in user_input:
                found_symptoms.append('depression')
            if 'anxiety' in user_input or 'anxious' in user_input or 'panic' in user_input:
                found_symptoms.append('anxiety')
        if 'joint' in found_symptoms:
            found_symptoms.append('arthritis')
        if 'skin' in found_symptoms:
            found_symptoms.append('skin_rash')
        if 'allergy' in found_symptoms:
            found_symptoms.append('allergies')
        if 'sleep' in found_symptoms:
            found_symptoms.append('insomnia')
        if 'back' in found_symptoms:
            found_symptoms.append('back_pain')
        if 'leg' in found_symptoms:
            found_symptoms.append('leg_pain')
        if 'hand' in found_symptoms:
            found_symptoms.append('hand_pain')
        if 'eye' in found_symptoms:
            found_symptoms.append('eye_problems')
        if 'dizziness' in found_symptoms:
            found_symptoms.append('dizziness')
        if 'diabetes' in found_symptoms:
            found_symptoms.append('diabetes')
        if 'blood_pressure' in found_symptoms:
            found_symptoms.append('hypertension')
        
        return list(set(found_symptoms))  # Remove duplicates
    
    def _assess_urgency(self, user_input: str) -> str:
        """Assess urgency level of symptoms"""
        user_input = user_input.lower()
        
        for urgency, patterns in self.condition_patterns.items():
            for pattern in patterns:
                if pattern in user_input:
                    return urgency
        
        return "general"
    
    def _generate_response(self, symptoms: List[str], urgency: str) -> str:
        """Generate appropriate response based on symptoms and urgency"""
        if urgency == "emergency":
            return self._emergency_response()
        elif urgency == "urgent":
            return self._urgent_response(symptoms)
        else:
            return self._general_response(symptoms)
    
    def _emergency_response(self) -> str:
        """Generate emergency response"""
        return ("🚨 **EMERGENCY - Seek Immediate Medical Attention**\n\n"
                "Based on your symptoms, this could be a medical emergency. "
                "Please call emergency services (108 in India, 911 in US) or go to the nearest emergency room immediately.\n\n"
                "Do not wait - emergency situations require immediate professional medical care.")
    
    def _urgent_response(self, symptoms: List[str]) -> str:
        """Generate urgent care response"""
        return ("⚠️ **URGENT - Medical Care Recommended**\n\n"
                "Based on your symptoms, you should seek medical attention soon. "
                "Please contact your doctor or visit an urgent care clinic within 24 hours.\n\n"
                f"Symptoms identified: {', '.join(symptoms)}\n\n"
                "While waiting for medical care: Rest, stay hydrated, and monitor your symptoms.")
    
    def _general_response(self, symptoms: List[str]) -> str:
        """Generate general advice response"""
        if not symptoms:
            return self._general_health_advice()
        
        responses = []
        for symptom in symptoms:
            # Direct mapping for specific conditions
            target_symptom = symptom
            
            # Map combined symptoms to proper knowledge base entries
            symptom_mapping = {
                'stomach_pain': 'stomach_pain',
                'chest_pain': 'chest_pain', 
                'breathing_difficulty': 'breathing_difficulty',
                'nausea_vomiting': 'nausea_vomiting',
                'depression': 'depression',
                'anxiety': 'anxiety',
                'arthritis': 'arthritis',
                'skin_rash': 'skin_rash',
                'allergies': 'allergies',
                'insomnia': 'insomnia',
                'back_pain': 'back_pain',
                'leg_pain': 'leg_pain',
                'hand_pain': 'hand_pain',
                'eye_problems': 'eye_problems',
                'dizziness': 'dizziness',
                'diabetes': 'diabetes',
                'hypertension': 'hypertension'
            }
            
            if symptom in symptom_mapping:
                target_symptom = symptom_mapping[symptom]
            elif symptom == 'headache' or symptom == 'head':
                target_symptom = 'headache'
            elif symptom == 'fever':
                target_symptom = 'fever'
            elif symptom == 'cough':
                target_symptom = 'cough'
            elif symptom == 'fatigue' or symptom == 'tired':
                target_symptom = 'fatigue'
            
            if target_symptom in self.knowledge_base:
                info = self.knowledge_base[target_symptom]
                response = f"<strong>{target_symptom.replace('_', ' ').title()} Management:</strong>\n\n"
                
                response += "<strong>• What might help:</strong>\n"
                for remedy in info["remedies"][:3]:  # Limit to top 3 remedies
                    response += f"  - {remedy}\n"
                
                if info["warning_signs"]:
                    response += f"\n<strong>• When to seek medical help:</strong>\n"
                    for warning in info["warning_signs"][:2]:  # Limit to top 2 warnings
                        response += f"  - {warning}\n"
                
                response += f"\n{info['disclaimer']}\n"
                responses.append(response)
        
        if not responses:
            return self._general_health_advice()
        
        return "\n".join(responses) + "\n\n<strong>Important:</strong> This advice is for informational purposes only and is not a substitute for professional medical care."
    
    def _general_health_advice(self) -> str:
        """Generate general health advice"""
        advice = [
            "🏥 **General Health Guidance**\n\n",
            "**For optimal health:**\n",
            "• Get 7-9 hours of quality sleep each night\n",
            "• Stay hydrated by drinking plenty of water\n",
            "• Eat a balanced diet rich in fruits and vegetables\n",
            "• Exercise regularly (150 minutes moderate activity per week)\n",
            "• Manage stress through relaxation techniques\n",
            "• Practice good hygiene and handwashing\n\n",
            "**When to see a doctor:**\n",
            "• Symptoms lasting more than a few days\n",
            "• Severe or worsening symptoms\n",
            "• Any concerns about your health\n\n",
            "**Disclaimer:** I'm an AI assistant and cannot provide medical diagnoses. "
            "Always consult with qualified healthcare professionals for medical concerns."
        ]
        return "".join(advice)
    
    def process_query(self, user_input: str) -> str:
        """Main method to process user queries"""
        # Clean and preprocess input
        user_input = user_input.strip().lower()
        
        # Check for AI identity questions
        identity_patterns = [
            "who are you", "what are you", "what is your name", 
            "are you human", "are you a bot", "are you an ai",
            "your identity", "introduce yourself", "tell me about yourself"
        ]
        
        for pattern in identity_patterns:
            if pattern in user_input:
                return self._ai_identity_response()
        
        # Check for diagnostic test visualization requests
        if "diagnostic test" in user_input or "test report" in user_input or "lab results" in user_input:
            if "graph" in user_input or "chart" in user_input or "visualization" in user_input:
                return self._diagnostic_test_response()
        
        # Assess urgency
        urgency = self._assess_urgency(user_input)
        
        # Extract symptoms
        symptoms = self._extract_symptoms(user_input)
        
        # Generate appropriate response
        response = self._generate_response(symptoms, urgency)
        
        return response
    
    def _ai_identity_response(self) -> str:
        """Generate AI identity response"""
        return ("🤖 **I am Medico AI, your intelligent health assistant**\n\n"
                "I am an artificial intelligence designed to provide general health information and guidance. "
                "I can help you understand various health conditions, symptoms, and provide general wellness advice.\n\n"
                "**What I can do:**\n"
                "• Provide information about common health conditions\n"
                "• Suggest general remedies for mild symptoms\n"
                "• Help you understand when to seek medical care\n"
                "• Offer preventive health tips\n\n"
                "**Important:** I am not a substitute for professional medical advice. "
                "Always consult with qualified healthcare professionals for diagnosis and treatment.\n\n"
                "How can I help with your health questions today?")
    
    def _diagnostic_test_response(self) -> str:
        """Generate diagnostic test visualization response"""
        return ("📊 **Diagnostic Test Visualization**\n\n"
                "I can help you understand your diagnostic test results through different visualization types:\n\n"
                "**Available Chart Options:**\n"
                "• **Line Graph** - Perfect for tracking trends over time (e.g., blood sugar levels, blood pressure)\n"
                "• **Bar Graph** - Ideal for comparing different values (e.g., cholesterol levels, vitamin counts)\n"
                "• **Pie Chart** - Best for showing proportions (e.g., blood cell distribution, risk factors)\n\n"
                "**To get your test report visualized:**\n"
                "1. Share your diagnostic test results\n"
                "2. Specify which type of chart you prefer\n"
                "3. Mention the time period if it's trend data\n\n"
                "**Example:** 'Show my blood pressure trends as a line graph for the past 6 months'\n\n"
                "Please share your test data and I'll create the appropriate visualization for you!")

# Initialize the AI instance
medical_ai = MedicalAI()

def get_medical_advice(user_input: str) -> str:
    """Public function to get medical advice"""
    return medical_ai.process_query(user_input)

if __name__ == "__main__":
    # Test the AI
    test_queries = [
        "I have a bad headache and fever",
        "My stomach hurts and I feel nauseous",
        "I'm having chest pain and difficulty breathing",
        "I feel tired all the time"
    ]
    
    for query in test_queries:
        print(f"Query: {query}")
        print(f"Response: {get_medical_advice(query)}")
        print("-" * 50)
