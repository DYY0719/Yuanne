with open(r'C:\Users\Encounter\Desktop\chat-app\templates\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Better typing indicator with animated dots
old_css = '''#typing-indicator {
    font-size: 12px;
    color: #999;
    margin-left: 10px;
    display: none;
    animation: blink 1.4s infinite;
}'''
new_css = '''#typing-indicator {
    font-size: 13px;
    color: #999;
    margin-left: 12px;
    display: none;
}
#typing-indicator .dot {
    display: inline-block;
    animation: blink 1.4s infinite;
    font-weight: bold;
}
#typing-indicator .dot:nth-child(2) { animation-delay: 0.2s; }
#typing-indicator .dot:nth-child(3) { animation-delay: 0.4s; }'''
content = content.replace(old_css, new_css)
print('1. CSS updated')

# 2. Update HTML: animated dots in the indicator
old_html = '<span id="typing-indicator">正在输入中...</span>'
new_html = '<span id="typing-indicator">正在输入中<span class="dot">.</span><span class="dot">.</span><span class="dot">.</span></span>'
content = content.replace(old_html, new_html)
print('2. HTML updated')

# 3. Increase delay from 700 to 1500
old_delay = 'showLinesStaggered(box, lines, 0, 700);'
new_delay = 'showLinesStaggered(box, lines, 0, 1500);'
content = content.replace(old_delay, new_delay)
print('3. Delay increased')

# 4. Add minimum 1s typing display
old_typing_hide = '''                        showTyping(false);
                        resetAutoTimer();'''
new_typing_hide = '''                        setTimeout(function() { showTyping(false); }, 1000);
                        resetAutoTimer();'''
if old_typing_hide in content:
    content = content.replace(old_typing_hide, new_typing_hide)
    print('4. Minimum typing display added')
else:
    print('4. FAIL: typing hide pattern not found')

with open(r'C:\Users\Encounter\Desktop\chat-app\templates\index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('All done.')
