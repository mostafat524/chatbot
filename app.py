# app.py - GROQ API VERSION (FREE & FAST)
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import time
import requests

app = Flask(__name__)
CORS(app)

class GazaAssistantWithGroq:
    def __init__(self):
        self.last_topic = None
        self.is_ai_ready = False
        self.groq_api_key = None
        self.setup_ai()
    
    def setup_ai(self):
        """Setup Groq API (free and fast!)"""
        # Get API key from environment or use default
        self.groq_api_key = os.environ.get("GROQ_API_KEY", "")
        
        if self.groq_api_key:
            self.is_ai_ready = True
            print("✅ Groq AI ready (Llama 3.2 - Free tier)")
        else:
            print("⚠️ No GROQ_API_KEY - Add it to Space secrets for AI chat")
            print("📋 Running in rule-based mode only")
    
    def get_ai_response(self, user_input, is_technical=False):
        """Use Groq API for AI responses"""
        if not self.is_ai_ready:
            return None
            
        try:
            # Different prompts for conversation vs technical
            if is_technical:
                system_prompt = """You are GAZA 101 - an expert humanitarian crisis assistant specializing in Gaza.

**Your Knowledge Base:**
- Water Crisis: 96% of water unfit for consumption, aquifer contamination, 15-20L/person/day
- Food Security: 93% face crisis-level insecurity, 30% child malnutrition, 65% farmland reduction
- Healthcare: 72% hospitals non-functional, 450k respiratory cases monthly
- Energy: 2-4 hours electricity daily, damaged infrastructure
- Environment: 450k tons CO2 from conflict, air quality 3x WHO limits
- Infrastructure: 60% buildings damaged, collapsed sanitation

**Your Role:**
- Provide accurate, compassionate information about Gaza's humanitarian crisis
- Offer practical, evidence-based solutions
- Be brief but informative (2-3 sentences max)
- Use emojis sparingly for readability
- If asked about solutions, suggest checking specific crisis areas"""
            else:
                system_prompt = """You are GAZA 101 - a friendly, compassionate AI assistant.

You're knowledgeable about Gaza's humanitarian situation but can also chat naturally about anything.

**Guidelines:**
- Be warm, natural, and engaging in conversations
- Keep casual responses SHORT (1-2 sentences)
- Use emojis occasionally 😊
- For Gaza questions, be informative but concise
- If technical Gaza questions come up, give brief answers and suggest exploring specific topics"""

            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.groq_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.2-90b-text-preview",  # Free tier, very capable
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 200,
                    "top_p": 0.9
                },
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                print(f"Groq API error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"AI error: {e}")
            return None

    def get_problem_description(self, topic):
        """Provide detailed problem descriptions - RULE BASED (Most Accurate)"""
        problems = {
            'water': """💧 **WATER CRISIS - The Problem**

**Critical Issues:**
• 96% of water in Gaza is unfit for human consumption
• Only 15-20 liters/person/day available (WHO minimum: 50-100 liters)
• Coastal aquifer is 70% over-extracted with severe seawater intrusion
• 85% of wastewater goes untreated, causing disease outbreaks

**Primary Challenges:**
- Aquifer contamination from conflict damage and sewage
- Damaged water infrastructure and distribution systems
- Limited electricity for water pumping and treatment
- High salinity levels (6x WHO safety standards)""",

            'food': """🌾 **FOOD SECURITY CRISIS - The Problem**

**Critical Issues:**
• 93% of Gaza's population faces crisis-level food insecurity
• 30% of children under 5 are acutely malnourished
• Local food production meets only 15% of population needs
• Food prices have increased 300% compared to pre-crisis

**Primary Challenges:**
- 65% reduction in arable land since 2000 (NASA data)
- Damaged agricultural infrastructure and irrigation systems
- Limited access to seeds, fertilizers, and farming equipment
- Disrupted supply chains and distribution networks""",

            'health': """🏥 **HEALTHCARE CRISIS - The Problem**

**Critical Issues:**
• 72% of hospitals in Gaza are non-functional
• Only 12 partially functioning hospitals for 2.3 million people
• Respiratory infections: 450,000 cases monthly
• Diarrheal diseases: 150,000 cases in children monthly

**Primary Challenges:**
- Critical shortage of medical supplies, equipment, and medicines
- 80% of children show trauma symptoms, 50% of adults report severe distress
- Overwhelmed remaining healthcare facilities
- Limited access to specialized care and emergency services""",

            'co2': """🌍 **CO2 & ENVIRONMENTAL CRISIS - The Problem**

**Critical Issues:**
• 450,000 tons of CO2 emissions from conflict activities (NASA data)
• Air quality: PM2.5 levels 45-65 μg/m³ (WHO safe limit: 15 μg/m³)
• 40% reduction in green spaces and carbon sequestration capacity
• Temperature increase of 1.2°C since 1990

**Primary Challenges:**
- Building destruction releasing concrete particulates and toxins
- Military operations consuming massive fuel resources
- Waste burning of plastics and hazardous materials
- Long-term environmental degradation and soil contamination""",

            'energy': """⚡ **ENERGY CRISIS - The Problem**

**Critical Issues:**
• Average 2-4 hours of electricity daily across Gaza
• Hospitals rely on unreliable generators for critical operations
• Water pumps often inoperative due to power shortages
• Limited fuel supplies for essential services

**Primary Challenges:**
- Damaged electrical grid infrastructure
- Limited access to reliable power sources
- High dependence on external fuel supplies
- Critical facilities operating at minimal capacity""",

            'infrastructure': """🏗️ **INFRASTRUCTURE CRISIS - The Problem**

**Critical Issues:**
• 60% of buildings damaged or destroyed in conflict areas
• Road networks severely damaged affecting aid delivery
• Communication infrastructure largely non-functional
• Sanitation systems collapsed leading to health hazards

**Primary Challenges:**
- Comprehensive damage to housing, schools, and public facilities
- Limited construction materials and equipment for rebuilding
- Coordination challenges for large-scale reconstruction
- Need for temporary shelter solutions for displaced populations"""
        }
        return problems.get(topic, "I can analyze water, food, health, energy, infrastructure, or environmental challenges.")
    
    def get_solutions(self, topic):
        """Provide actionable solutions - RULE BASED"""
        solutions = {
            'water': """🚰 **WATER CRISIS SOLUTIONS**

**Immediate Actions (0-2 weeks):**
• Distribute chlorine tablets (1 tablet per 20L water) - 2 weeks
• Deploy portable filtration units in high-risk areas - 2 weeks
• Establish emergency water distribution points - 1 week

**Short-term Solutions (2-8 weeks):**
• Install rainwater harvesting systems - 1 month
• Repair damaged water infrastructure - 2 months
• Implement community water safety monitoring - 3 weeks

**Materials Needed:** Chlorine tablets, ceramic filters, polyethylene tanks, solar panels""",

            'food': """🌱 **FOOD SECURITY SOLUTIONS**

**Immediate Actions (0-2 weeks):**
• Distribute ready-to-use therapeutic food - Immediate
• Establish emergency community kitchens - 2 weeks
• Provide nutrition supplements - 1 week

**Short-term Solutions (2-8 weeks):**
• Start vertical farming - 6 weeks
• Implement urban agriculture - 2 months

**Materials Needed:** RUTF packets, hydroponic kits, seeds, gardening tools""",

            'health': """🏥 **HEALTHCARE SOLUTIONS**

**Immediate Actions (0-2 weeks):**
• Deploy mobile trauma units - 2 weeks
• Distribute emergency medical kits - 1 week
• Establish mental health first aid - 2 weeks

**Short-term Solutions (2-8 weeks):**
• Set up telemedicine networks - 1 month
• Train community health workers - 3 weeks

**Materials Needed:** Medical equipment, telemedicine terminals, medicines""",

            'co2': """🌿 **CO2 MITIGATION SOLUTIONS**

**Immediate Actions (0-2 weeks):**
• Establish waste management systems - 2 weeks
• Distribute clean cooking technologies - 1 week
• Launch air quality monitoring - 1 week

**Short-term Solutions (2-8 weeks):**
• Implement solar energy microgrids - 1 month
• Start reforestation programs - 2 months

**Materials Needed:** Solar panels, waste management equipment, native saplings""",

            'energy': """⚡ **ENERGY SOLUTIONS**

**Immediate Actions (0-2 weeks):**
• Distribute portable power banks - 2 weeks
• Deploy solar-powered lighting - 1 week
• Provide generators to critical facilities - Immediate

**Short-term Solutions (2-8 weeks):**
• Install solar microgrids - 1 month
• Implement energy-efficient designs - 2 months

**Materials Needed:** Solar panels, batteries, power banks""",

            'infrastructure': """🏗️ **INFRASTRUCTURE SOLUTIONS**

**Immediate Actions (0-2 weeks):**
• Set up temporary shelters - 2 weeks
• Establish basic sanitation - 1 week
• Repair critical access roads - 2 weeks

**Short-term Solutions (2-8 weeks):**
• Rebuild damaged schools - 3 months
• Restore communication networks - 2 months

**Materials Needed:** Temporary shelters, construction materials, sanitation equipment"""
        }
        return solutions.get(topic, "I have solutions for water, food, health, energy, infrastructure, and environmental challenges.")
    
    def detect_topic(self, user_input):
        """Detect which crisis topic the user is asking about"""
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ['water', 'drink', 'thirst', 'aquifer']):
            return 'water'
        elif any(word in user_lower for word in ['food', 'hunger', 'nutrition', 'farming', 'agriculture']):
            return 'food'
        elif any(word in user_lower for word in ['health', 'medical', 'hospital', 'doctor', 'healthcare']):
            return 'health'
        elif any(word in user_lower for word in ['co2', 'carbon', 'emission', 'environment', 'pollution', 'air quality']):
            return 'co2'
        elif any(word in user_lower for word in ['energy', 'power', 'solar', 'electric', 'electricity']):
            return 'energy'
        elif any(word in user_lower for word in ['infrastructure', 'building', 'construction', 'road', 'shelter', 'house']):
            return 'infrastructure'
        else:
            return None
    
    def is_gaza_question(self, user_input):
        """Check if user is asking about Gaza specifically"""
        user_lower = user_input.lower()
        gaza_keywords = [
            'gaza', 'palestine', 'conflict', 'crisis', 'humanitarian',
            'war', 'occupation', 'blockade', 'siege'
        ]
        return any(keyword in user_lower for keyword in gaza_keywords)
    
    def is_conversational_query(self, user_input):
        """Check if this is casual conversation"""
        user_lower = user_input.lower().strip()
        
        conversational_phrases = [
            'how are you', 'can we talk', 'thank you', 'thanks', 
            'who are you', 'what are you', 'hello', 'hi', 'hey',
            'good morning', 'good afternoon', 'good evening',
            'what can you do', 'help me', 'tell me about yourself'
        ]
        
        if user_lower in ['hi', 'hello', 'hey', 'yo']:
            return True
            
        if any(phrase in user_lower for phrase in conversational_phrases):
            return True
            
        if len(user_lower.split()) <= 3 and not self.detect_topic(user_input):
            return True
            
        return False

    def get_response(self, user_input):
        user_lower = user_input.lower().strip()
        
        # Welcome message
        if not user_input.strip():
            return """🌍 **GAZA 101 - Hybrid Crisis Assistant**

Hi! I'm your AI-powered humanitarian assistant with dual intelligence:

🤖 **AI Chat** - Natural conversations + Gaza knowledge (Powered by Groq)
📋 **Technical Data** - Verified crisis statistics & solutions
⚡ **Lightning Fast** - Free tier, production ready

**Crisis Areas I Cover:**
💧 Water | 🌾 Food | 🏥 Health | ⚡ Energy | 🏗️ Infrastructure | 🌍 CO2

**Try asking:**
• "Tell me about the water situation in Gaza"
• "How can we help with food security?"
• "What are the energy challenges?"
• Or just chat naturally! 😊"""
        
        # Handle solution requests
        if any(word in user_lower for word in ['yes', 'yeah', 'sure', 'please', 'solution', 'how can']) and self.last_topic:
            solutions = self.get_solutions(self.last_topic)
            self.last_topic = None
            return solutions
        
        if any(word in user_lower for word in ['no', 'not now', 'later', 'maybe later']) and self.last_topic:
            self.last_topic = None
            if self.is_ai_ready:
                ai_response = self.get_ai_response("User declined solutions, respond friendly", False)
                if ai_response:
                    return ai_response
            return "No problem! 😊 What else would you like to know?"
        
        # PRIORITY 1: Detailed technical queries → Rule-based (most accurate)
        topic = self.detect_topic(user_input)
        if topic and len(user_input.split()) > 4:  # Detailed query
            self.last_topic = topic
            problem_text = self.get_problem_description(topic)
            return problem_text + "\n\n**Would you like me to provide specific solutions for this challenge?**"
        
        # PRIORITY 2: Gaza questions → AI (it has context)
        if self.is_gaza_question(user_input) and self.is_ai_ready:
            ai_response = self.get_ai_response(user_input, is_technical=True)
            if ai_response:
                return ai_response + "\n\n💡 *Ask about specific areas (water/food/health/energy/infrastructure/CO2) for detailed data!*"
        
        # PRIORITY 3: Simple topic mention → Brief AI + offer details
        if topic and self.is_ai_ready:
            ai_response = self.get_ai_response(f"Give a 1-sentence overview of {topic} crisis in Gaza", is_technical=True)
            if ai_response:
                return ai_response + f"\n\n**Want detailed statistics and solutions for {topic}? Just ask!** 📊"
        
        # PRIORITY 4: Casual conversation → AI
        if self.is_conversational_query(user_input) and self.is_ai_ready:
            ai_response = self.get_ai_response(user_input, is_technical=False)
            if ai_response:
                return ai_response
        
        # PRIORITY 5: General questions → AI
        if self.is_ai_ready:
            ai_response = self.get_ai_response(user_input, is_technical=False)
            if ai_response:
                return ai_response
        
        # Fallback (no API key)
        return """😊 **I'm here to help!**

I can provide detailed information about:
💧 Water crisis | 🌾 Food security | 🏥 Healthcare
⚡ Energy | 🏗️ Infrastructure | 🌍 Environment

*Note: Add GROQ_API_KEY to enable AI conversations!*
For now, I can answer with accurate technical data. Try asking about a specific crisis area!"""

# Initialize assistant
assistant = GazaAssistantWithGroq()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'response': 'Please send a message.'}), 400
            
        user_message = data.get('message', '')
        print(f"User: {user_message}")
        
        start_time = time.time()
        response = assistant.get_response(user_message)
        response_time = (time.time() - start_time) * 1000
        
        print(f"Bot: {response[:100]}...")
        print(f"⏱️ Response: {response_time:.1f}ms")
        
        return jsonify({'response': response})
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'response': 'Hello! I\'m GAZA 101. How can I help you today?'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 7860))
    print("🚀 Starting GAZA 101 Assistant...")
    print("🤖 Powered by Groq (Free Llama 3.2)")
    print("📋 Rule-based backup system active")
    print(f"🔗 Server on port {port}")
    app.run(debug=False, host='0.0.0.0', port=port)