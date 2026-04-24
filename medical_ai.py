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
        """Load medical knowledge base"""
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
            }
        }
    
    def _load_symptom_keywords(self) -> Dict[str, List[str]]:
        """Load symptom keyword mappings"""
        return {
            "headache": ["headache", "head", "migraine", "pain in head", "throbbing"],
            "fever": ["fever", "temperature", "hot", "chills", "sweating", "feverish"],
            "cough": ["cough", "coughing", "chesty", "dry cough", "throat"],
            "stomach": ["stomach", "abdomen", "belly", "tummy", "gut", "digestive", "stomach ache", "stomach pain", "abdominal pain", "belly ache", "tummy pain"],
            "pain": ["pain", "ache", "hurt", "sore", "discomfort", "uncomfortable"],
            "fatigue": ["tired", "fatigue", "exhausted", "weak", "no energy", "sleepy"],
            "nausea": ["nausea", "queasy", "sick", "vomit", "throw up", "upset stomach"]
        }
    
    def _load_condition_patterns(self) -> Dict[str, List[str]]:
        """Load condition recognition patterns"""
        return {
            "emergency": [
                "chest pain", "difficulty breathing", "severe pain", "bleeding",
                "unconscious", "confusion", "stroke", "heart attack"
            ],
            "urgent": [
                "high fever", "persistent vomiting", "severe headache", "broken bone",
                "deep wound", "poisoning", "allergic reaction"
            ],
            "general": [
                "cold", "flu", "headache", "stomach ache", "minor pain", "fatigue"
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
            # Check for combined symptoms (like stomach + pain = stomach_pain)
            combined_symptom = None
            if 'stomach' in symptoms and 'pain' in symptoms:
                combined_symptom = 'stomach_pain'
            elif 'headache' in symptoms or 'head' in symptoms:
                combined_symptom = 'headache'
            
            # Use combined symptom if available, otherwise use individual symptom
            target_symptom = combined_symptom if combined_symptom and combined_symptom in self.knowledge_base else symptom
            
            if target_symptom in self.knowledge_base:
                info = self.knowledge_base[target_symptom]
                response = f"<strong>{symptom.title()} Management:</strong>\n\n"
                
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
        user_input = user_input.strip()
        
        # Assess urgency
        urgency = self._assess_urgency(user_input)
        
        # Extract symptoms
        symptoms = self._extract_symptoms(user_input)
        
        # Generate appropriate response
        response = self._generate_response(symptoms, urgency)
        
        return response

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
