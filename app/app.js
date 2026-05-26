/* 
    SmartClinics AI - App Logic Simulation
    This file mocks up the real-time AI capabilities, translation latency, 
    and emergency detection features for the prototype.
*/

// Dictionary to simulate translation for the demo
const translationDictionary = {
    // English -> Spanish / Target
    "Hello, I'm Dr. Chen. How are you feeling today?": "Hola, soy la Dra. Chen. ¿Cómo se siente hoy?",
    "I understand. Let's get that checked out.": "Entiendo. Vamos a revisar eso.",
    "Are you currently taking any medications?": "¿Está tomando algún medicamento actualmente?",
    "Take this twice a day after meals.": "Tome esto dos veces al día después de las comidas.",
    
    // Fallbacks
    "default_dr": "Simulated translation output for this medical term.",
    
    // Patient responses (Mock target -> English)
    "Spanish": {
        "Me duele mucho el pecho al respirar.": "I am having a lot of chest pain when I breathe deeply.",
        "No, no tomo medicinas.": "No, I am not taking any medications.",
        "Gracias, doctora.": "Thank you, doctor."
    },
    "Mandarin": {
        "default": "I've been feeling very dizzy since yesterday morning."
    },
    // Emergency Trigger phrases
    "emergency_triggers": ["chest pain", "can't breathe", "heart attack", "suicide", "bleeding heavily"]
};

// Generate a mock response from the patient based on language
function generateMockResponse(lang) {
    if (lang === 'Spanish') {
        return "Me duele mucho el pecho al respirar.";
    }
    return "This is a simulated patient response in " + lang;
}

// Generate the translation string 
function generateMockTranslation(text, targetLang) {
    if (targetLang === 'Spanish' && translationDictionary[text]) {
        return translationDictionary[text];
    }
    return `[Translated to ${targetLang}]: ${text}`;
}

// Check for emergency keywords
function checkForEmergency(englishText) {
    const textLower = englishText.toLowerCase();
    const hasEmergency = translationDictionary.emergency_triggers.some(trigger => textLower.includes(trigger));
    
    if (hasEmergency) {
        const banner = document.getElementById('emergencyBanner');
        if (banner) {
            banner.style.display = 'flex';
            // Scroll to top to see it
            document.getElementById('chatContainer').scrollTop = 0;
            
            // Auto hide after 10s for demo
            setTimeout(() => {
                banner.style.display = 'none';
            }, 10000);
        }
    }
}

// Add a message to the UI
function addMessageToChat(role, originalText, translationLang, translatedText) {
    const container = document.getElementById('chatContainer');
    if (!container) return;

    // Create wrapper
    const msgDiv = document.createElement('div');
    msgDiv.className = `message-group ${role === 'doc' ? 'msg-doc' : 'msg-patient'}`;
    
    // Add Speaker label
    const speakerLabel = document.createElement('div');
    speakerLabel.className = 'msg-speaker';
    speakerLabel.innerText = role === 'doc' ? 'Dr. Chen (English)' : `Patient (${translationLang})`;
    
    // Add Bubble
    const bubble = document.createElement('div');
    bubble.className = 'msg-bubble';
    
    // Text content
    const primaryText = document.createElement('div');
    primaryText.innerText = originalText;
    
    // Subtitle translation
    const subText = document.createElement('div');
    subText.className = 'msg-translation';
    subText.innerText = translatedText;

    // Assemble visually
    bubble.appendChild(primaryText);
    bubble.appendChild(subText);
    msgDiv.appendChild(speakerLabel);
    msgDiv.appendChild(bubble);

    // Initial state hidden for animation
    msgDiv.style.opacity = '0';
    msgDiv.style.transform = role === 'doc' ? 'translateX(20px)' : 'translateX(-20px)';
    msgDiv.style.transition = 'all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1)';
    
    container.appendChild(msgDiv);
    
    // Trigger animation
    setTimeout(() => {
        msgDiv.style.opacity = '1';
        msgDiv.style.transform = 'translateX(0)';
        // Scroll to bottom
        container.scrollTop = container.scrollHeight;
    }, 10);
    
    // Check emergency if it's english text (doc speaking or patient translated to English)
    const textToCheck = role === 'doc' ? originalText : translatedText;
    checkForEmergency(textToCheck);
}

// Create typing indicator element
function createTypingIndicator(role) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message-group ${role === 'doc' ? 'msg-doc' : 'msg-patient'}`;
    msgDiv.id = 'activeTypingIndicator';
    
    const bubble = document.createElement('div');
    bubble.className = 'msg-bubble typing-indicator';
    bubble.innerHTML = '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';
    
    msgDiv.appendChild(bubble);
    return msgDiv;
}

// Handle form submission (Doctor typing/speaking demo)
function handleDemoSubmit(e) {
    e.preventDefault();
    const input = document.getElementById('demoInput');
    const text = input.value.trim();
    if (!text) return;
    
    input.value = '';
    
    // Get target lang
    const targetLang = new URLSearchParams(window.location.search).get('lang') || 'Spanish';
    const translatedText = generateMockTranslation(text, targetLang);
    
    // 1. Immediately show Doctor's original text (Wait for translation)
    const container = document.getElementById('chatContainer');
    
    // Show AI "translating" indicator
    const typing = createTypingIndicator('doc');
    container.appendChild(typing);
    container.scrollTop = container.scrollHeight;
    
    // 2. Simulate Latency (approx 400-800ms)
    const latency = Math.random() * 400 + 400;
    
    setTimeout(() => {
        // Remove typing indicator
        if (document.getElementById('activeTypingIndicator')) {
            document.getElementById('activeTypingIndicator').remove();
        }
        
        // Add full message
        addMessageToChat('doc', text, targetLang, translatedText);
        
        // 3. Trigger Mock Patient Reply after a delay (if patient link notification is active, don't auto reply immediately)
        setTimeout(() => {
            simulatePatientReply(targetLang);
        }, 4000);
        
    }, latency);
}

// Simulates the patient responding
function simulatePatientReply(lang) {
    const container = document.getElementById('chatContainer');
    
    // Show patient typing/speaking
    const typing = createTypingIndicator('patient');
    container.appendChild(typing);
    container.scrollTop = container.scrollHeight;
    
    setTimeout(() => {
        if (document.getElementById('activeTypingIndicator')) {
            document.getElementById('activeTypingIndicator').remove();
        }
        
        // "I understand. Let's get that checked out" is a good generic follow-up response
        // In the static demo we use hardcoded spanish responses.
        const original = "No entiendo muy bien las instrucciones.";
        const englishTranslation = "I don't understand the instructions very well.";
        
        addMessageToChat('patient', original, lang, englishTranslation);
    }, 1500);
}

// Simulated Microphone Interaction
const simMicBtn = document.getElementById('simMicBtn');
if (simMicBtn) {
    simMicBtn.addEventListener('mousedown', () => {
        simMicBtn.classList.add('recording');
        document.getElementById('demoInput').placeholder = "Listening... Release to translate";
    });
    
    simMicBtn.addEventListener('mouseup', () => {
        simMicBtn.classList.remove('recording');
        document.getElementById('demoInput').placeholder = "Type to simulate speaking (Demo)...";
        // Auto fill demo text
        document.getElementById('demoInput').value = "Are you currently taking any medications?";
        handleDemoSubmit(new Event('submit'));
    });
    
    // Handle touch
    simMicBtn.addEventListener('touchstart', (e) => {
        e.preventDefault();
        simMicBtn.classList.add('recording');
    });
    simMicBtn.addEventListener('touchend', (e) => {
        e.preventDefault();
        simMicBtn.classList.remove('recording');
        document.getElementById('demoInput').value = "Are you currently taking any medications?";
        handleDemoSubmit(new Event('submit'));
    });
}

// ── Mobile sidebar off-canvas toggle ──────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.querySelector('.sidebar-toggle');
    const sidebar   = document.querySelector('.sidebar');
    const backdrop  = document.querySelector('.sidebar-backdrop');
    if (!toggleBtn || !sidebar) return;

    function openSidebar() {
        sidebar.classList.add('open');
        if (backdrop) backdrop.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
    function closeSidebar() {
        sidebar.classList.remove('open');
        if (backdrop) backdrop.classList.remove('active');
        document.body.style.overflow = '';
    }

    toggleBtn.addEventListener('click', () =>
        sidebar.classList.contains('open') ? closeSidebar() : openSidebar()
    );
    if (backdrop) backdrop.addEventListener('click', closeSidebar);

    // Auto-close sidebar when a nav link is tapped on mobile
    document.querySelectorAll('.nav-item').forEach(item =>
        item.addEventListener('click', () => {
            if (window.innerWidth <= 768) closeSidebar();
        })
    );
});
