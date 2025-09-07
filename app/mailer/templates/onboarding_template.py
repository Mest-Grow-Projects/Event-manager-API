from .base_template import email_template

def onboarding_email_template(name: str) -> str:
    content = f"""
    <div class="content">
        <h2>Account Verified successfully</h1>
        <p>Hello {name},</p>
        <p>
            Welcome to <strong>Event Hive</strong> — we’re thrilled to have you on board!  
            You’ve just unlocked access to a vibrant community where <strong>events come alive</strong>.
        </p>
        <h3>Here’s what you can do now:</h3>
        <ul>
            <li>📅 <strong>Discover</strong> trending events, concerts, and festivals near you.</li>
            <li>🎟 <strong>Secure tickets</strong> instantly with our seamless booking system.</li>
            <li>🤝 <strong>Connect</strong> with organizers and like-minded attendees.</li>
            <li>🌍 <strong>Create</strong> your own events and share them with the world.</li>
        </ul>
        <div style="margin: 25px 0; text-align: center;">
            <a href="https://eventhive.com/login" 
               style="background-color:#10107B; color:#ffffff; padding:14px 28px; border-radius:6px; text-decoration:none; font-weight:bold; font-size:15px; display:inline-block;">
               🚀 Get Started Now
            </a>
        </div>
        <p>
            We can’t wait to see the amazing experiences you’ll discover and share.  
            Your journey with <strong>Event Hive</strong> starts today!
        </p>
        <p>Best regards,<br>The Event Hive Team</p>
    </div>
    """

    return email_template(content)