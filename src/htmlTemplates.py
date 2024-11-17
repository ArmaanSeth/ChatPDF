css = '''
<style>
    :root {
        --base-bg: #1e1e1e;
        --user-gradient-start: #3a3a3a;
        --user-gradient-end: #5a5a5a;
        --bot-gradient-start: #2a2a2a;
        --bot-gradient-end: #4a4a4a;
        --message-bg: #333333;
        --text-color: #f0f0f0;
        --accent-color: #7f8c8d;
        --shadow-color: rgba(0, 0, 0, 0.5);
        --highlight-color: rgba(255, 255, 255, 0.1);
        --neon-glow: #a8ff78;
        --avatar-size: 60px;
    }

    body {
        font-family: 'Roboto', sans-serif;
        background-color: var(--base-bg);
        color: var(--text-color);
    }

    .chat-message {
        padding: 1rem;
        border-radius: 1rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        position: relative;
        background: var(--base-bg);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        overflow: hidden;
    }

    .chat-message::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, var(--neon-glow) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .chat-message:hover::before {
        opacity: 0.1;
    }

    .chat-message:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px var(--shadow-color);
    }

    .chat-message.user {
        justify-content: flex-end;
        background: linear-gradient(135deg, var(--user-gradient-start), var(--user-gradient-end));
    }

    .chat-message.bot {
        justify-content: flex-start;
        background: linear-gradient(135deg, var(--bot-gradient-start), var(--bot-gradient-end));
    }

    .chat-message .avatar {
        width: var(--avatar-size);
        height: var(--avatar-size);
        margin: 0 1rem;
        position: relative;
        z-index: 1;
    }

    .chat-message .avatar img {
        max-width: 100%;
        max-height: 100%;
        border-radius: 50%;
        object-fit: cover;
        box-shadow: 0 4px 8px var(--shadow-color);
        border: 3px solid var(--accent-color);
        transition: transform 0.3s ease, border-color 0.3s ease;
    }

    .chat-message .avatar img:hover {
        transform: rotate(360deg) scale(1.1);
        border-color: var(--neon-glow);
    }

    .chat-message .message {
        max-width: 70%;
        padding: 1rem;
        color: var(--text-color);
        border-radius: 0.8rem;
        background: var(--message-bg);
        box-shadow: 4px 4px 8px var(--shadow-color), -4px -4px 8px var(--highlight-color);
        position: relative;
        z-index: 1;
        overflow: hidden;
    }

    .chat-message .message::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, var(--highlight-color), transparent);
        transition: left 0.5s;
    }

    .chat-message:hover .message::after {
        left: 100%;
    }

    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(168, 255, 120, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(168, 255, 120, 0); }
        100% { box-shadow: 0 0 0 0 rgba(168, 255, 120, 0); }
    }

    .chat-message:hover .avatar img {
        animation: pulse 1.5s infinite;
    }
</style>

'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://cdn-icons-png.flaticon.com/512/6134/6134346.png">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="message">{{MSG}}</div>
    <div class="avatar">
        <img src="https://png.pngtree.com/png-vector/20190321/ourmid/pngtree-vector-users-icon-png-image_856952.jpg">
    </div>    
</div>
'''
