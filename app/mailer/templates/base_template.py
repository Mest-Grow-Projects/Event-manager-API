from datetime import datetime


def email_template (content: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="utf-8"/>
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
      <title>Event Hive</title>
      <style>
        * {{
          margin: 0;
          padding: 0;
          box-sizing: border-box;
        }}
    
        body {{
          font-family: 'Arial', sans-serif;
          line-height: 1.6;
          background-color: #F5F6FA;
          color: #2B2B2B;
        }}
    
        .container {{
          max-width: 600px;
          margin: 40px auto;
          background: #ffffff;
          border-radius: 8px;
          overflow: hidden;
          box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }}
    
        .header {{
          text-align: center;
          background-color: #10107B;
          color: #ffffff;
          font-size: 28px;     
          font-weight: bold;  
          letter-spacing: 1px;   
          padding: 20px;   
        }}
    
        .content {{
          padding: 30px;
          font-size: 15px;
          background-color: #fff;
          color: #333333;
        }}
        
        .verification-code {{
          background-color: #F4F6FF;
          padding: 15px;
          margin: 20px 0;
          border-radius: 5px;
          text-align: center;
          font-size: 22px;
          letter-spacing: 5px;
          font-weight: bold;
          color: #10107B;
        }}
    
        .warning {{
          background-color: #FFF3CD;
          border-left: 5px solid #EE9322;
          padding: 14px;
          margin: 20px 0;
          border-radius: 4px;
          font-size: 14px;
          color: #856404;
        }}
    
        .footer {{
          background: #0B0C10;
          color: #B0B3B8;
          text-align: center;
          padding: 20px;
          font-size: 12px;
        }}
    
        .footer a {{
          color: #FBC500;
          text-decoration: none;
          margin: 0 8px;
        }}
    
        h1, h2, h3 {{
          color: #10107B;
          font-size: 20px;
        }}
    
        p {{
          margin-bottom: 14px;
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">Event Hive</div>
        <div class="content">
            ${content}
        </div>
        <div class="footer">
            <p>© {datetime.now().year} Event Hive. All rights reserved.</p>
            <p>This is an automated message. Do not reply directly to this email.</p>
            <p>Proudly powered by: <a href="#" target="_blank">Event Hive</a> </p>
            <p>
            <a href="#privacy">Privacy Policy</a> | 
            <a href="#terms">Terms of Service</a> | 
            <a href="#contact">Contact</a>
            </p>
        </div>
      </div>
    </body>
    </html>
    """