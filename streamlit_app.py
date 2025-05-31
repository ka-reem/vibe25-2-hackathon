#!/usr/bin/env python3
"""
🎯 Referral Bounty Hunter - Streamlit Frontend
Turn your friend group into a bounty hunting squad!
"""

import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import subprocess
import sys

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from llama_client import LlamaProcessor
except ImportError:
    st.error("⚠️ LlamaProcessor not available. Some features may be limited.")

# Configure page
st.set_page_config(
    page_title="Referral Bounty Hunter",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern look
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .hero-text {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    .bounty-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #4ecdc4;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .success-message {
        background: linear-gradient(90deg, #56ab2f, #a8e6cf);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
    }
    
    .warning-message {
        background: linear-gradient(90deg, #ff9a56, #ffad56);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🎯 Referral Bounty Hunter</h1>', unsafe_allow_html=True)
    st.markdown('''
    <div class="hero-text">
        <strong>Turn your friend group into a bounty hunting squad!</strong><br>
        High-paying jobs offer referral rewards — sometimes $20k+ — but most people never hear about them.<br>
        We're flipping that. No HR. No gatekeeping. Just referrals, rewards, and receipts. 💰
    </div>
    ''', unsafe_allow_html=True)
    
    # Sidebar for navigation
    with st.sidebar:
        st.image("https://via.placeholder.com/200x80/4ecdc4/white?text=BOUNTY+HUNTER", width=200)
        
        page = st.selectbox(
            "🎯 Choose Your Mission",
            ["🏠 Bounty Dashboard", "🔍 Scout Talent", "💼 Job Fit Analysis", "💬 Intel Chat", "🏆 Leaderboard"]
        )
        
        st.markdown("---")
        st.markdown("### 🎮 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Active Bounties", "12", "↗️ 3")
        with col2:
            st.metric("Total Rewards", "$45K", "↗️ $8K")
    
    # Main content based on page selection
    if page == "🏠 Bounty Dashboard":
        show_dashboard()
    elif page == "🔍 Scout Talent":
        show_talent_scout()
    elif page == "💼 Job Fit Analysis":
        show_job_fit()
    elif page == "💬 Intel Chat":
        show_intel_chat()
    elif page == "🏆 Leaderboard":
        show_leaderboard()

def show_dashboard():
    """Main dashboard with bounty overview"""
    st.markdown("## 🎯 Active Bounties")
    
    # Sample bounty data
    bounties = [
        {"company": "OpenAI", "role": "Senior AI Engineer", "bounty": "$25,000", "deadline": "2025-06-15", "status": "🔥 Hot"},
        {"company": "Anthropic", "role": "Research Scientist", "bounty": "$20,000", "deadline": "2025-06-30", "status": "🎯 Active"},
        {"company": "Google", "role": "Staff SWE", "bounty": "$15,000", "deadline": "2025-07-01", "status": "🎯 Active"},
        {"company": "Meta", "role": "ML Engineer", "bounty": "$18,000", "deadline": "2025-06-20", "status": "⏰ Urgent"},
    ]
    
    # Display bounties in cards
    for i, bounty in enumerate(bounties):
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        
        with col1:
            st.markdown(f"**{bounty['company']}** - {bounty['role']}")
        with col2:
            st.markdown(f"💰 **{bounty['bounty']}**")
        with col3:
            st.markdown(f"📅 {bounty['deadline']}")
        with col4:
            st.markdown(bounty['status'])
        
        if st.button(f"🎯 Hunt This Bounty", key=f"hunt_{i}"):
            st.session_state.selected_bounty = bounty
            st.success(f"Selected {bounty['company']} {bounty['role']} bounty!")
    
    st.markdown("---")
    
    # Analytics section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Bounty Analytics")
        
        # Sample data for chart
        companies = ['OpenAI', 'Anthropic', 'Google', 'Meta', 'Stripe']
        bounty_amounts = [25000, 20000, 15000, 18000, 12000]
        
        fig = px.bar(
            x=companies, 
            y=bounty_amounts,
            title="Top Bounties by Company",
            color=bounty_amounts,
            color_continuous_scale="viridis"
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Success Rate")
        
        # Pie chart for success rates
        labels = ['Successful Referrals', 'In Progress', 'Missed']
        values = [35, 45, 20]
        colors = ['#4ecdc4', '#45b7d1', '#ff6b6b']
        
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
        fig.update_traces(marker=dict(colors=colors))
        fig.update_layout(title="Referral Success Rate")
        st.plotly_chart(fig, use_container_width=True)

def show_talent_scout():
    """Talent scouting page"""
    st.markdown("## 🔍 Scout Talent")
    st.markdown("Find the perfect candidate for your bounty hunt!")
    
    # LinkedIn URL input
    linkedin_url = st.text_input(
        "🔗 LinkedIn Profile URL",
        placeholder="https://www.linkedin.com/in/username",
        help="Enter a LinkedIn profile URL to scout this person"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Scout This Person", type="primary"):
            if linkedin_url:
                with st.spinner("🕵️ Scouting talent... This may take a moment"):
                    success = run_crustdata_fetch(linkedin_url)
                    if success:
                        st.markdown('<div class="success-message">✅ Talent scouted successfully!</div>', unsafe_allow_html=True)
                        st.rerun()
                    else:
                        st.markdown('<div class="warning-message">❌ Scouting failed. Check your API credentials.</div>', unsafe_allow_html=True)
            else:
                st.warning("Please enter a LinkedIn URL first!")
    
    with col2:
        if st.button("📄 Load Sample Data"):
            # Load existing data if available
            if os.path.exists("person_data.json"):
                st.success("✅ Sample data loaded!")
            else:
                st.info("No sample data available. Scout someone first!")
    
    # Display current scouted person if data exists
    if os.path.exists("person_data.json"):
        with open("person_data.json", 'r') as f:
            person_data = json.load(f)
        
        if person_data:
            person = person_data[0] if isinstance(person_data, list) else person_data
            
            st.markdown("---")
            st.markdown("## 🎯 Current Scout Target")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("### 👤 Basic Info")
                st.write(f"**Name:** {person.get('name', 'Unknown')}")
                st.write(f"**Title:** {person.get('current_position_title', 'Unknown')}")
                st.write(f"**Company:** {person.get('current_company_name', 'Unknown')}")
            
            with col2:
                st.markdown("### 💼 Experience")
                if 'work_experience' in person:
                    for exp in person['work_experience'][:3]:
                        st.write(f"• {exp.get('employee_title', 'Unknown')} at {exp.get('employer_name', 'Unknown')}")
            
            with col3:
                st.markdown("### 🎓 Education")
                if 'education_background' in person:
                    for edu in person['education_background'][:2]:
                        degree = edu.get('degree_name', 'Unknown')
                        school = edu.get('institute_name', 'Unknown')
                        st.write(f"• {degree} from {school}")

def show_job_fit():
    """Job fit analysis page"""
    st.markdown("## 💼 Job Fit Analysis")
    st.markdown("Analyze if your scouted talent is perfect for a specific bounty!")
    
    # Check if person data exists
    if not os.path.exists("person_data.json"):
        st.warning("🔍 No scouted talent found! Go to the Scout Talent page first.")
        return
    
    # Job description input
    job_description = st.text_area(
        "📋 Job Description",
        placeholder="Paste the job description here...",
        height=200,
        help="Enter the complete job description for analysis"
    )
    
    if st.button("🎯 Analyze Job Fit", type="primary"):
        if job_description.strip():
            with st.spinner("🤖 AI is analyzing the job fit..."):
                processor = LlamaProcessor()
                analysis = processor.analyze_job_fit(job_description)
                
                st.markdown("---")
                st.markdown("## 🎯 Analysis Results")
                st.markdown(analysis)
        else:
            st.warning("Please enter a job description first!")
    
    # Quick bounty templates
    st.markdown("---")
    st.markdown("### 🚀 Quick Bounty Templates")
    
    templates = {
        "Senior Software Engineer": "We're looking for a Senior Software Engineer with 5+ years of experience in Python, JavaScript, and cloud technologies. Experience with microservices, Docker, and Kubernetes required.",
        "AI/ML Engineer": "Seeking an AI/ML Engineer with expertise in deep learning, PyTorch/TensorFlow, and production ML systems. PhD preferred but not required.",
        "Product Manager": "Looking for a Product Manager with 3+ years experience in B2B SaaS products. Strong analytical skills and experience with user research required.",
        "Data Scientist": "We need a Data Scientist with expertise in statistical modeling, SQL, Python, and business intelligence. Experience with A/B testing preferred."
    }
    
    selected_template = st.selectbox("Choose a template:", list(templates.keys()))
    if st.button("📋 Use Template"):
        st.session_state.job_template = templates[selected_template]
        st.rerun()
    
    if 'job_template' in st.session_state:
        st.text_area("Template loaded:", value=st.session_state.job_template, height=100)

def show_intel_chat():
    """Intelligence chat interface"""
    st.markdown("## 💬 Intel Chat")
    st.markdown("Ask questions about your scouted talent!")
    
    # Check if person data exists
    if not os.path.exists("person_data.json"):
        st.warning("🔍 No scouted talent found! Go to the Scout Talent page first.")
        return
    
    # Load person data
    with open("person_data.json", 'r') as f:
        person_data = json.load(f)
    
    person = person_data[0] if isinstance(person_data, list) else person_data
    
    # Display current target
    st.markdown("### 🎯 Current Intel Target")
    st.info(f"**{person.get('name', 'Unknown')}** - {person.get('current_position_title', 'Unknown')} at {person.get('current_company_name', 'Unknown')}")
    
    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask anything about this person..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("🤖 Analyzing intel..."):
                processor = LlamaProcessor()
                
                # Create a simple prompt with the person data and user question
                full_prompt = f"""
                Based on the following person data, please answer the user's question:

                Person Data:
                {json.dumps(person, indent=2)}

                User Question: {prompt}

                Please provide a helpful and accurate answer based on the data above.
                """
                
                try:
                    completion = processor.client.chat.completions.create(
                        model="Llama-4-Maverick-17B-128E-Instruct-FP8",
                        messages=[{"role": "user", "content": full_prompt}],
                    )
                    response = completion.choices[0].message.content
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"Error getting intel: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

def show_leaderboard():
    """Leaderboard page"""
    st.markdown("## 🏆 Bounty Hunter Leaderboard")
    st.markdown("See who's crushing it in the referral game!")
    
    # Sample leaderboard data
    leaderboard_data = [
        {"rank": 1, "hunter": "Alex Chen", "successful_referrals": 12, "total_earnings": "$95,000", "success_rate": "85%"},
        {"rank": 2, "hunter": "Sarah Kim", "successful_referrals": 10, "total_earnings": "$78,000", "success_rate": "82%"},
        {"rank": 3, "hunter": "Mike Johnson", "successful_referrals": 8, "total_earnings": "$65,000", "success_rate": "80%"},
        {"rank": 4, "hunter": "Emma Davis", "successful_referrals": 7, "total_earnings": "$52,000", "success_rate": "77%"},
        {"rank": 5, "hunter": "David Liu", "successful_referrals": 6, "total_earnings": "$48,000", "success_rate": "75%"},
    ]
    
    # Display leaderboard
    for hunter in leaderboard_data:
        col1, col2, col3, col4, col5 = st.columns([1, 3, 2, 2, 2])
        
        with col1:
            if hunter["rank"] == 1:
                st.markdown("🥇")
            elif hunter["rank"] == 2:
                st.markdown("🥈")
            elif hunter["rank"] == 3:
                st.markdown("🥉")
            else:
                st.markdown(f"#{hunter['rank']}")
        
        with col2:
            st.markdown(f"**{hunter['hunter']}**")
        with col3:
            st.markdown(f"🎯 {hunter['successful_referrals']} referrals")
        with col4:
            st.markdown(f"💰 {hunter['total_earnings']}")
        with col5:
            st.markdown(f"📊 {hunter['success_rate']}")
    
    # Personal stats
    st.markdown("---")
    st.markdown("### 🎮 Your Stats")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Your Rank", "#7", "↗️ 2")
    with col2:
        st.metric("Successful Referrals", "4", "↗️ 1")
    with col3:
        st.metric("Total Earnings", "$32,000", "↗️ $8K")
    with col4:
        st.metric("Success Rate", "72%", "↗️ 5%")

def run_crustdata_fetch(linkedin_url=None):
    """Run the crustdata.py script to fetch person data"""
    try:
        if linkedin_url:
            result = subprocess.run([sys.executable, "crustdata.py", linkedin_url], 
                                  capture_output=True, text=True, cwd=os.getcwd())
        else:
            result = subprocess.run([sys.executable, "crustdata.py"], 
                                  capture_output=True, text=True, cwd=os.getcwd())
        
        return result.returncode == 0
    except Exception as e:
        st.error(f"Error running talent scout: {str(e)}")
        return False

if __name__ == "__main__":
    main()
