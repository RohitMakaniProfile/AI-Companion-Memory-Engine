import streamlit as st
import os
import json
import re
from typing import Dict, List
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config - must be first Streamlit command
st.set_page_config(
    page_title="AI Companion Memory & Personality Engine",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #6b7280;
        text-align: center;
        margin-bottom: 2rem;
    }
    .memory-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .emotion-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .fact-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .chat-message {
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        line-height: 1.6;
    }
    .user-message {
        background-color: #dbeafe;
        border-left: 4px solid #3b82f6;
    }
    .bot-message {
        background-color: #f3f4f6;
        border-left: 4px solid #6b7280;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


# Azure OpenAI Client Setup
@st.cache_resource
def get_azure_client():
    """Initialize Azure OpenAI client with credentials"""
    try:
        return AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
    except Exception as e:
        st.error(f"Error initializing Azure Client: {e}")
        return None


# Sample Realistic Conversation Data (30 messages)
SAMPLE_CONVERSATIONS = [
    {"role": "user", "content": "Yaar, I'm so stressed about my JEE mains next month. Can't sleep properly."},
    {"role": "assistant", "content": "Arre, exam stress bohot common hai. Neend kharab ho rahi hai kya? Tell me more."},
    {"role": "user", "content": "Haan yaar, raat ko 2-3 baje tak padhta hoon phir subah 6 baje uthna padta hai."},
    {"role": "assistant",
     "content": "That's only 3-4 hours of sleep! Your brain needs rest to retain information. Have you tried a fixed sleep schedule?"},
    {"role": "user", "content": "I tried but fir bhi darr lagta hai ki enough prep nahi ho raha."},
    {"role": "assistant",
     "content": "Anxiety makes you feel unprepared even when you've studied well. Kya tum mock tests de rahe ho?"},
    {"role": "user", "content": "Haan, but scores inconsistent hai. Sometimes 180/300, sometimes 220/300."},
    {"role": "assistant",
     "content": "That actually shows you have the knowledge. Consistency will come with better rest and less panic."},
    {"role": "user", "content": "My parents are also pressuring me for 250+ score. Unka kuch nahi ho sakta."},
    {"role": "assistant",
     "content": "Parent pressure is real. But remember, they want your success, not your suffering. Talk to them once?"},
    {"role": "user",
     "content": "Nahi yaar, they won't understand. Papa engineer hai, unhone first attempt mein crack kiya tha."},
    {"role": "assistant", "content": "Their journey was different. Your effort is equally valid. Don't compare beta."},
    {"role": "user", "content": "Sometimes I feel like giving up. Engineering ke alawa kuch nahi dikhta future mein."},
    {"role": "assistant",
     "content": "Feeling hopeless is a sign you're burned out. Take a day off - guilt free. Your mind needs it."},
    {"role": "user", "content": "Break? Exam toh next month hai! How can I take break?"},
    {"role": "assistant",
     "content": "One day won't ruin your prep, but burnout will ruin your exam performance. Trust me on this."},
    {"role": "user",
     "content": "Okay maybe... Also, meri girlfriend hai, vo bhi upset hai because I don't give her time."},
    {"role": "assistant",
     "content": "Relationships during prep phase are tough. Have you explained your situation to her?"},
    {"role": "user",
     "content": "Haan but she thinks I'm avoiding her. We used to talk daily, ab 2-3 days mein ek baar."},
    {"role": "assistant",
     "content": "That's a valid concern from her side. Maybe schedule one fixed call per day? 15 minutes bhi enough hai."},
    {"role": "user", "content": "Good idea. I'll try that. Thanks yaar."},
    {"role": "assistant", "content": "Good! Small steps matter. Now tell me, what subjects are you weakest in?"},
    {"role": "user", "content": "Physics is okay, Chemistry bhi manage ho jaati hai, but Maths... specially calculus."},
    {"role": "assistant",
     "content": "Calculus needs practice, not cramming. Do 10 problems daily instead of 50 weekly. Consistency > Intensity."},
    {"role": "user", "content": "Hmm makes sense. I usually avoid it and then do marathon sessions on weekends."},
    {"role": "assistant", "content": "Exactly! That's why it feels hard. Daily touch keeps concepts fresh."},
    {"role": "user", "content": "Okay I'll try this new approach. Feeling slightly better after talking."},
    {"role": "assistant", "content": "I'm glad! Remember - you're more prepared than you think. Believe in yourself."},
    {"role": "user", "content": "Thanks didi. One last thing - kya meditation actually helps ya time waste hai?"},
    {"role": "assistant",
     "content": "Meditation = brain training. Even 5 minutes daily can reduce anxiety significantly. Try it!"},
    {"role": "user", "content": "Okay will give it a shot. You've been really helpful today."},
    {"role": "assistant", "content": "Always here for you beta. Now go, ace that prep! All the best! 💪"}
]


class MemoryExtractor:
    """Extracts meaningful patterns from user conversations"""

    def __init__(self, client, deployment_name):
        self.client = client
        self.deployment = deployment_name

    def extract_memories(self, conversations: List[Dict]) -> Dict:
        """Extract preferences, emotions, and facts from conversations"""

        # Prepare conversation text
        conv_text = "\n".join(
            [f"{'User' if msg['role'] == 'user' else 'Bot'}: {msg['content']}" for msg in conversations])

        extraction_prompt = f"""Analyze the following conversation and extract:
        1. USER PREFERENCES (likes, dislikes, interests, habits)
        2. EMOTIONAL PATTERNS (stress triggers, anxiety sources, coping mechanisms)
        3. IMPORTANT FACTS (relationships, goals, deadlines, challenges)

        Conversation:
        {conv_text}

        Provide output in valid JSON format:
        {{
            "preferences": ["preference1", "preference2", ...],
            "emotional_patterns": ["pattern1", "pattern2", ...],
            "facts": ["fact1", "fact2", ...]
        }}
        """

        try:
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=[
                    {"role": "system",
                     "content": "You are an expert at analyzing conversations and extracting psychological insights. Output valid JSON only."},
                    {"role": "user", "content": extraction_prompt}
                ],
                temperature=0.3,
                max_tokens=800,
                response_format={"type": "json_object"}
            )

            result_text = response.choices[0].message.content
            return json.loads(result_text)

        except Exception as e:
            # Fallback if API fails
            st.warning(f"Live extraction failed ({str(e)}). Using fallback data.")
            return self._fallback_extraction()

    def _fallback_extraction(self):
        """Simple rule-based extraction as fallback"""
        return {
            "preferences": [
                "Prefers studying late at night",
                "Values relationship with girlfriend",
                "Struggles with mathematics particularly calculus"
            ],
            "emotional_patterns": [
                "High exam-related anxiety",
                "Parent pressure causing stress",
                "Fear of failure and comparison",
                "Burnout from overwork"
            ],
            "facts": [
                "Preparing for JEE Mains exam next month",
                "Father is an engineer who cleared exam in first attempt",
                "Currently sleeping only 3-4 hours per night",
                "Mock test scores range from 180-220 out of 300",
                "Has girlfriend who feels neglected due to exam prep"
            ]
        }


class PersonalityEngine:
    """Generates responses with different personality styles"""

    PERSONALITIES = {
        "Calm Mentor": {
            "system_prompt": """You are a wise, experienced mentor who speaks with calm authority and patience.
            Your responses are:
            - Measured and thoughtful
            - Use analogies and wisdom from experience
            - Speak in complete, well-structured sentences
            - Professional yet warm tone
            - Focus on long-term growth and perspective
            Keep responses concise (2-3 sentences max).""",
            "color": "#10b981",
            "icon": "🧘"
        },
        "Witty Friend": {
            "system_prompt": """You are a fun, witty best friend who uses humor to lighten heavy situations.
            Your responses are:
            - Casual and conversational (use slang like 'Bro', 'Scene', 'Chill')
            - Include light jokes or playful teasing
            - Use modern slang and informal language
            - Add emoji occasionally
            - Keep it real and relatable
            Keep responses concise (2-3 sentences max).""",
            "color": "#f59e0b",
            "icon": "😄"
        },
        "Therapist": {
            "system_prompt": """You are a professional therapist trained in CBT and active listening.
            Your responses are:
            - Empathetic and validating
            - Ask reflective questions
            - Use therapeutic language ("I hear that...", "It sounds like...")
            - Focus on feelings and underlying emotions
            - Non-judgmental and supportive
            Keep responses concise (2-3 sentences max).""",
            "color": "#8b5cf6",
            "icon": "🤝"
        }
    }

    def __init__(self, client, deployment_name):
        self.client = client
        self.deployment = deployment_name

    def generate_response(self, user_message: str, personality: str, context: str = "") -> str:
        """Generate response with specified personality"""

        if personality not in self.PERSONALITIES:
            return "Invalid personality selected."

        personality_config = self.PERSONALITIES[personality]

        messages = [
            {"role": "system", "content": personality_config["system_prompt"]}
        ]

        if context:
            messages.append({"role": "system", "content": f"Context about user: {context}"})

        messages.append({"role": "user", "content": user_message})

        try:
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=messages,
                temperature=0.7,
                max_tokens=200
            )
            return response.choices[0].message.content

        except Exception as e:
            return f"Error generating response: {str(e)}"


def display_memory_insights(memories: Dict):
    """Display extracted memories in beautiful cards"""

    st.markdown("<h2 style='text-align: center; margin-top: 2rem;'>🧠 Memory Extraction Results</h2>",
                unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #667eea;">👤 Preferences</h3>
            <h1>{len(memories.get('preferences', []))}</h1>
            <p>patterns identified</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #f5576c;">💭 Emotions</h3>
            <h1>{len(memories.get('emotional_patterns', []))}</h1>
            <p>patterns detected</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #00f2fe;">📌 Facts</h3>
            <h1>{len(memories.get('facts', []))}</h1>
            <p>facts remembered</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Detailed insights
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<div class='memory-card'>", unsafe_allow_html=True)
        st.markdown("### 👤 User Preferences")
        for pref in memories.get('preferences', []):
            st.markdown(f"• {pref}")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='emotion-card'>", unsafe_allow_html=True)
        st.markdown("### 💭 Emotional Patterns")
        for emotion in memories.get('emotional_patterns', []):
            st.markdown(f"• {emotion}")
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("<div class='fact-card'>", unsafe_allow_html=True)
        st.markdown("### 📌 Important Facts")
        for fact in memories.get('facts', []):
            st.markdown(f"• {fact}")
        st.markdown("</div>", unsafe_allow_html=True)


def display_personality_comparison(engine: PersonalityEngine, test_message: str, context: str):
    """Show side-by-side personality response comparison"""

    st.markdown("<h2 style='text-align: center; margin-top: 2rem;'>🎭 Personality Engine Comparison</h2>",
                unsafe_allow_html=True)
    st.markdown(f"<div class='chat-message user-message'><strong>User Message:</strong> {test_message}</div>",
                unsafe_allow_html=True)

    st.markdown("---")

    cols = st.columns(3)

    for idx, (personality_name, config) in enumerate(PersonalityEngine.PERSONALITIES.items()):
        with cols[idx]:
            with st.spinner(f"Generating {personality_name} response..."):
                response = engine.generate_response(test_message, personality_name, context)

            st.markdown(f"""
            <div style="border: 3px solid {config['color']}; border-radius: 12px; padding: 1.5rem; background: white; min-height: 200px;">
                <h3 style="color: {config['color']};">{config['icon']} {personality_name}</h3>
                <p style="line-height: 1.8; margin-top: 1rem; color: #374151; font-size: 1.05rem;">
                    {response}
                </p>
            </div>
            """, unsafe_allow_html=True)


def main():
    # Header
    st.markdown("<h1 class='main-header'>🧠 AI Companion: Memory & Personality Engine</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Extract user insights and transform conversation styles with AI</p>",
                unsafe_allow_html=True)

    # Initialize clients
    client = get_azure_client()
    if not client:
        st.warning("Azure Client not initialized. Please check API keys in .env file.")
        st.stop()

    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4")

    memory_extractor = MemoryExtractor(client, deployment)
    personality_engine = PersonalityEngine(client, deployment)

    # Sidebar
    with st.sidebar:
        st.markdown("## 📊 Assignment Info")
        st.markdown("""
        This demo showcases:
        - **Memory Extraction** from 30 conversations
        - **Personality Engine** with 3 distinct styles
        - **Before/After Comparison** of response tones
        """)

        st.markdown("---")
        st.markdown("### ⚙️ Settings")

        show_raw_data = st.checkbox("Show Raw Conversation Data", value=False)

        st.markdown("---")
        st.markdown(f"""
        <div style='text-align: center; color: #6b7280; font-size: 0.9rem;'>
            <p>Built with Azure OpenAI</p>
            <p>Deployment: {deployment}</p>
        </div>
        """, unsafe_allow_html=True)

    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📖 Overview", "🧠 Memory Extraction", "🎭 Personality Engine", "⚖️ Comparison"])

    with tab1:
        st.markdown("### Welcome to the AI Companion Demo")
        st.markdown("""
        This application demonstrates advanced AI capabilities for companion applications:

        #### 🎯 Key Features:

        1. **Memory Extraction Module**
           - Analyzes 30+ chat messages to identify patterns
           - Extracts user preferences, emotional patterns, and important facts
           - Uses structured AI prompting for accurate insights

        2. **Personality Engine**
           - Three distinct conversation styles: Calm Mentor, Witty Friend, Therapist
           - Same content, different emotional delivery
           - Context-aware responses using extracted memories

        3. **Comparison View**
           - Side-by-side personality response comparison
           - Highlights how tone affects user experience
           - Real-time generation with Azure OpenAI

        #### 🚀 How to Use:
        - Navigate through tabs to explore features
        - Memory Extraction shows insights from sample conversations
        - Personality Engine lets you test different response styles
        - Comparison view shows all three personalities simultaneously
        """)

        st.markdown("---")
        st.info("💡 **Tip**: Check the 'Memory Extraction' tab first to see what the AI learned about the user!")

    with tab2:
        st.markdown("### Analyzing Sample Conversation...")

        if st.button("🚀 Run Memory Extraction"):
            with st.spinner("Extracting memories from 30 messages..."):
                memories = memory_extractor.extract_memories(SAMPLE_CONVERSATIONS)
                st.session_state['memories'] = memories  # Store for other tabs
                display_memory_insights(memories)

        elif 'memories' in st.session_state:
            display_memory_insights(st.session_state['memories'])
        else:
            st.info("Click the button above to analyze the conversation.")

        if show_raw_data:
            st.markdown("---")
            st.markdown("### 📜 Raw Conversation Data")
            for msg in SAMPLE_CONVERSATIONS:
                if msg['role'] == 'user':
                    st.markdown(f"<div class='chat-message user-message'><strong>User:</strong> {msg['content']}</div>",
                                unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='chat-message bot-message'><strong>Bot:</strong> {msg['content']}</div>",
                                unsafe_allow_html=True)

    with tab3:
        st.markdown("### Test the Personality Engine")
        st.markdown("Enter a user message and select a personality to see how the AI responds.")

        col1, col2 = st.columns([2, 1])

        with col1:
            test_input = st.text_area(
                "User Message:",
                value="I'm feeling really overwhelmed with everything. Don't know where to start.",
                height=100
            )

        with col2:
            selected_personality = st.selectbox(
                "Choose Personality:",
                list(PersonalityEngine.PERSONALITIES.keys())
            )

        use_context = st.checkbox("Use extracted memories as context", value=True)

        if st.button("🎯 Generate Response", use_container_width=True):
            context = ""
            if use_context:
                if 'memories' not in st.session_state:
                    # Auto run extraction if not done yet
                    st.session_state['memories'] = memory_extractor.extract_memories(SAMPLE_CONVERSATIONS)

                # Create a summary string from the memory dict
                mem = st.session_state['memories']
                context = f"User Facts: {', '.join(mem.get('facts', []))}. Emotions: {', '.join(mem.get('emotional_patterns', []))}."

            with st.spinner(f"Generating {selected_personality} response..."):
                response = personality_engine.generate_response(test_input, selected_personality, context)

            config = PersonalityEngine.PERSONALITIES[selected_personality]

            st.markdown("---")
            st.markdown(f"### {config['icon']} {selected_personality} Response:")
            st.markdown(f"""
            <div style="border-left: 5px solid {config['color']}; padding: 1.5rem; background: #f9fafb; border-radius: 8px; font-size: 1.1rem; line-height: 1.8;">
                {response}
            </div>
            """, unsafe_allow_html=True)

    with tab4:
        st.markdown("### Compare All Personalities Side-by-Side")

        comparison_message = st.text_area(
            "Enter a message to see how each personality responds:",
            value="I failed my mock test again. I'm thinking maybe engineering isn't for me.",
            height=100
        )

        use_memory_context = st.checkbox("Include user context from memory extraction", value=True, key="comp_check")

        if st.button("🔄 Generate All Responses", use_container_width=True):
            context = ""
            if use_memory_context:
                if 'memories' not in st.session_state:
                    st.session_state['memories'] = memory_extractor.extract_memories(SAMPLE_CONVERSATIONS)
                mem = st.session_state['memories']
                context = f"User Facts: {', '.join(mem.get('facts', []))}. Emotions: {', '.join(mem.get('emotional_patterns', []))}."

            display_personality_comparison(personality_engine, comparison_message, context)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #6b7280; padding: 2rem;'>
        <p>🧠 <strong>AI Companion Memory & Personality Engine</strong></p>
        <p>Powered by Azure OpenAI GPT-4</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()