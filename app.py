import streamlit as st
import os
import time
import random
import base64
from modules.ocr import extract_text_from_image
from modules.pdf_processor import extract_text_from_pdf
from modules.nlp_processor import extract_medical_data
from modules.analyzer import analyze_medical_data
from modules.recommender import get_recommendations
from modules.translator import LANGUAGES, get_ui_label, translate_text
from utils.file_handler import save_uploaded_file, delete_file
import pandas as pd

# 1. Page Config
st.set_page_config(
    page_title="SmartMed AI",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Interactive Background Logic (HTML/JS/CSS)
particle_animation_html = """
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Create Canvas
    var canvas = document.createElement('canvas');
    canvas.id = 'particle-canvas';
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    canvas.style.zIndex = '-1';
    canvas.style.pointerEvents = 'none'; // Allow clicks to pass through
    document.body.appendChild(canvas);

    var ctx = canvas.getContext('2d');
    var width, height;
    var particles = [];

    // Particle Configuration
    var particleCount = window.innerWidth < 768 ? 40 : 80; // Fewer on mobile
    var connectionDistance = 120;
    var mouseDistance = 150;

    function resize() {
        width = window.innerWidth;
        height = window.innerHeight;
        canvas.width = width;
        canvas.height = height;
    }
    window.addEventListener('resize', resize);
    resize();

    // Mouse Tracking
    var mouse = { x: null, y: null };
    window.addEventListener('mousemove', function(e) {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
    });
    window.addEventListener('mouseout', function() {
        mouse.x = null;
        mouse.y = null;
    });

    // Particle Class
    function Particle() {
        this.x = Math.random() * width;
        this.y = Math.random() * height;
        this.vx = (Math.random() - 0.5) * 0.5;
        this.vy = (Math.random() - 0.5) * 0.5;
        this.size = Math.random() * 2 + 1;
        this.baseColor = 'rgba(46, 134, 193, '; // Blue tint
    }

    Particle.prototype.update = function() {
        this.x += this.vx;
        this.y += this.vy;

        // Bounce off edges
        if (this.x < 0 || this.x > width) this.vx *= -1;
        if (this.y < 0 || this.y > height) this.vy *= -1;

        // Mouse Attraction (Cluster effect)
        if (mouse.x != null) {
            var dx = mouse.x - this.x;
            var dy = mouse.y - this.y;
            var distance = Math.sqrt(dx*dx + dy*dy);

            if (distance < mouseDistance) {
                var forceDirectionX = dx / distance;
                var forceDirectionY = dy / distance;
                var force = (mouseDistance - distance) / mouseDistance;
                var attractionStrength = 0.03;

                this.vx += forceDirectionX * force * attractionStrength;
                this.vy += forceDirectionY * force * attractionStrength;
            }
        }
        
        // Dampen velocity to prevent explosion
        var speed = Math.sqrt(this.vx*this.vx + this.vy*this.vy);
        if(speed > 2) {
            this.vx *= 0.95;
            this.vy *= 0.95;
        }
    };

    Particle.prototype.draw = function() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fillStyle = this.baseColor + '0.4)';
        ctx.fill();
    };

    // Initialize Particles
    for (var i = 0; i < particleCount; i++) {
        particles.push(new Particle());
    }

    // Animation Loop
    function animate() {
        ctx.clearRect(0, 0, width, height);
        
        // Update and Draw Particles
        for (var i = 0; i < particles.length; i++) {
            particles[i].update();
            particles[i].draw();

            // Draw Connections (optional, keeping it subtle: only near mouse)
            if (mouse.x != null) {
                var dx = mouse.x - particles[i].x;
                var dy = mouse.y - particles[i].y;
                var dist = Math.sqrt(dx*dx + dy*dy);
                
                if (dist < connectionDistance) {
                    ctx.beginPath();
                    ctx.strokeStyle = 'rgba(46, 134, 193, ' + (1 - dist/connectionDistance)*0.2 + ')';
                    ctx.lineWidth = 1;
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(mouse.x, mouse.y);
                    ctx.stroke();
                }
            }
        }
        requestAnimationFrame(animate);
    }
    
    // Start only if performance isn't terrible (basic check)
    if (navigator.hardwareConcurrency > 1) {
        animate();
    }
});
</script>
"""

# Inject CSS/JS
st.markdown(particle_animation_html, unsafe_allow_html=True)
st.markdown("""
<style>
    /* 1. Reset & Global Base */
    html, body, [class*="css"] {
        font-family: 'Open Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #2c3e50;
    }
    h1, h2, h3 {
        font-family: 'Montserrat', sans-serif;
    }

    /* 2. Hide Streamlit Chrome */
    [data-testid="stSidebar"] { display: none; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stDeployButton { display: none; }

    /* 3. Clean Main Background */
    .stApp {
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%); /* Clean Light Gray/White Gradient */
    }

    /* 4. Glassmorphism Container */
    .block-container {
        padding: 3rem 2rem;
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(12px); /* Frosted Glass Effect */
        -webkit-backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.4);
        max-width: 900px;
        margin: auto;
        margin-top: 2rem;
    }

    /* 5. Header Styling */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid rgba(0,0,0,0.05);
    }
    .app-title {
        font-size: 2rem;
        font-weight: 700;
        color: #2E86C1;
        margin: 0;
    }
    .app-subtitle {
        color: #7f8c8d;
        font-size: 0.9rem;
        margin-top: 0.2rem;
    }

    /* 6. Feature Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.03);
    }
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(46, 134, 193, 0.15);
        border-color: #2E86C1;
    }
    
    /* 7. Button Styling */
    div.stButton > button {
        background: linear-gradient(90deg, #2E86C1 0%, #00d2ff 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.7rem 2rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(46, 134, 193, 0.3);
        width: 100%;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(46, 134, 193, 0.4);
    }

    /* 8. Upload Box Styling */
    [data-testid='stFileUploader'] {
        border-radius: 12px;
        padding: 1rem;
        border: 2px dashed #aab7b8;
        background: rgba(255,255,255,0.5);
        transition: border-color 0.3s;
    }
    [data-testid='stFileUploader']:hover {
        border-color: #2E86C1;
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        color: #2E86C1;
    }
</style>
""", unsafe_allow_html=True)

# 3. Custom Header Layout (Simulating a specific Top Bar)
# We can't put Streamlit widgets literally inside custom HTML divs easily, so we use columns.
top_col1, top_col2 = st.columns([3, 1])

with top_col1:
    st.markdown("""
        <div>
            <div class="app-title">🩺 SmartMed AI</div>
            <div class="app-subtitle">Intelligent Medical Report Analysis & Guidance</div>
        </div>
    """, unsafe_allow_html=True)

with top_col2:
    # Language Selector (Right aligned via Column layout)
    selected_lang_name = st.selectbox("Select Language", list(LANGUAGES.keys()), label_visibility="collapsed")
    lang_code = LANGUAGES[selected_lang_name]

st.markdown("---")

# 4. Main Content Area
uploaded_file = st.file_uploader("Upload Medical Report", type=["pdf", "jpg", "png", "jpeg"], label_visibility="collapsed")

# Configure basic logging for the app
import logging
logging.basicConfig(
    filename='app.log', 
    filemode='a', 
    format='%(asctime)s - %(levelname)s - %(message)s', 
    level=logging.ERROR
)
logger = logging.getLogger(__name__)

from modules.validator import validate_medical_report
from utils.feedback_manager import save_feedback

if uploaded_file is None:
    # --- Landing Page ---
    st.markdown(f"<p style='text-align: center; color: #666; margin-top: -10px;'>{get_ui_label('upload_label', lang_code)}</p>", unsafe_allow_html=True)
    st.write("") # Spacer

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="glass-card">
            <h3>📑</h3>
            <h4>Upload</h4>
            <p style="font-size:0.85rem; color:#666;">Securely upload your PDF or Image lab reports.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3>🔍</h3>
            <h4>Analyze</h4>
            <p style="font-size:0.85rem; color:#666;">Advanced OCR extracts and standardizes your data.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="glass-card">
            <h3>🛡️</h3>
            <h4>Privacy</h4>
            <p style="font-size:0.85rem; color:#666;">Your data is processed in-memory and deleted instantly.</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br><br>", unsafe_allow_html=True)

else:
    # --- Analysis Pipeline ---
    progress_bar = st.progress(0)
    status_msg = st.empty()
    
    file_path = save_uploaded_file(uploaded_file, "uploads")
    
    status_msg.markdown(f"**⏳ {get_ui_label('extracting_img', lang_code)}...**" if "pdf" not in uploaded_file.name else f"**⏳ {get_ui_label('extracting_pdf', lang_code)}...**")
    progress_bar.progress(10)
    
    try:
        # 1. Extraction
        if uploaded_file.name.lower().endswith(".pdf"):
            extracted_text = extract_text_from_pdf(file_path)
        else:
            extracted_text = extract_text_from_image(file_path)
            
        progress_bar.progress(30)

        # Robust check for extraction failure
        if extracted_text is None:
             status_msg.error("⚠️ Failed to process file. It might be corrupted or in an unsupported format.")
             logger.error(f"Extraction returned None for file: {uploaded_file.name}")
        elif not extracted_text.strip():
             status_msg.warning("⚠️ No text found. Please upload a clearer PDF or Image.")
             logger.warning(f"Extraction returned empty text for file: {uploaded_file.name}")
        else:
            # 2. Validation Layer
            status_msg.markdown("**🔍 Validating document content...**")
            is_valid, score, details = validate_medical_report(extracted_text)
            
            if not is_valid:
                progress_bar.empty()
                status_msg.error("⚠️ This document does not appear to be a valid medical lab report.")
                st.info("Please upload a standard document containing medical test results (e.g., Hemoglobin, Glucose, Lipid Profile).")
                with st.expander("Details (Why was this rejected?)"):
                    st.write(f"Confidence Score: {score} (Threshold: 15)")
                    st.write("We look for medical terms (e.g., Blood, Hemoglobin) and units (e.g., mg/dL).")
                logger.warning(f"Validation failed for {uploaded_file.name}. Score: {score}")
            
            else:
                progress_bar.progress(50)
                
                # 3. NLP Analysis
                status_msg.markdown("**🧠 Analyzing medical data...**")
                medical_data = extract_medical_data(extracted_text)
                progress_bar.progress(70)
                
                if medical_data:
                    analyzed_data = analyze_medical_data(medical_data)
                    
                    # Translation with Fallback
                    if lang_code != "en":
                         for item in analyzed_data:
                            item["interpretation"] = translate_text(item["interpretation"], lang_code)
                    
                    df = pd.DataFrame(analyzed_data)
                    progress_bar.progress(100)
                    time.sleep(0.5)
                    progress_bar.empty()
                    status_msg.empty()
                
                    # --- Result Display ---
                    st.toast("Analysis Complete!", icon="🩺")
                    
                    st.markdown(f"### {get_ui_label('results_title', lang_code)}")

                    
                    # Summary Stats
                    issues = df[df['status'].isin(['High', 'Low'])].shape[0]
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Tests Found", len(df))
                    c2.metric("Normal Range", len(df) - issues)
                    c3.metric("Attention Needed", issues, delta_color="inverse")
                    
                    st.divider()
                    
                    # Detailed Table
                    def highlight(val):
                        if val == 'Normal': return 'color: #27ae60; font-weight: bold;'
                        elif val in ['High', 'Low']: return 'color: #c0392b; font-weight: bold;'
                        return ''

                    st.dataframe(
                        df.style.map(highlight, subset=['status']),
                        width='stretch',
                        hide_index=True
                    )
                    
                    # Recommendations
                    recommendations = get_recommendations(analyzed_data)
                    if recommendations:
                        st.divider()
                        st.markdown(f"### {get_ui_label('rec_title', lang_code)}")
                        st.info(get_ui_label("rec_intro", lang_code))
                        
                        for test, recs in recommendations.items():
                            color = "#e74c3c" if recs['status'] in ['High', 'Low'] else "#27ae60"
                            
                            st.markdown(f"""
                            <div style="background: rgba(255,255,255,0.8); border-left: 5px solid {color}; padding: 15px; border-radius: 10px; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                                <h4 style="color: {color}; margin: 0;">{test} ({recs['status']})</h4>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            colA, colB, colC = st.columns(3)
                            with colA:
                                st.caption(f"**{get_ui_label('foods', lang_code)}**")
                                for i in recs['foods']: st.write(f"• {translate_text(i, lang_code)}")
                            with colB:
                                st.caption(f"**{get_ui_label('lifestyle', lang_code)}**")
                                for i in recs['lifestyle']: st.write(f"• {translate_text(i, lang_code)}")
                            with colC:
                                st.caption(f"**{get_ui_label('avoid', lang_code)}**")
                                for i in recs['avoid']: st.write(f"• {translate_text(i, lang_code)}")

                else:
                     status_msg.warning(get_ui_label("no_data", lang_code))

    except Exception:
        status_msg.error("An internal error occurred.")
    
    # --- Feedback Section ---
    st.markdown("---")
    st.markdown(f"##### 💬 {get_ui_label('feedback_title', lang_code)}")
    
    # We use a form to prevent reload on every keystroke
    with st.form("feedback_form"):
        col_fb1, col_fb2 = st.columns([1, 3])
        with col_fb1:
            helpful = st.radio("Helpful?", ["Yes", "No"], horizontal=True, label_visibility="collapsed")
        with col_fb2:
            comment = st.text_input("Optional Comment", placeholder="Tell us more...", label_visibility="collapsed")
            
        submit_feedback = st.form_submit_button("Submit Feedback")
        
        if submit_feedback:
            save_feedback(helpful, comment)
            st.success("Thank you for your feedback!")
            time.sleep(1.5) # Let user see the message
    if st.button("Start New Analysis"):
        delete_file(file_path)
        st.rerun()

# 5. Footer (Simple Copyright)
st.markdown("""
<div style="text-align: center; margin-top: 40px; color: #95a5a6; font-size: 0.8rem;">
    SmartMed AI © 2026<br>
    Disclaimer: Not a medical device. Use for info only.
</div>
""", unsafe_allow_html=True)
