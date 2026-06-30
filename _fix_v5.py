import re

with open(r'C:\Users\Encounter\Desktop\chat-app\templates\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the sendMessage function start and the function after it (updateSendBtn)
start = content.find('async function sendMessage()')
end = content.find('\nfunction updateSendBtn()')

if start < 0 or end < 0:
    print('FAIL: could not find sendMessage or updateSendBtn')
    exit()

new_sendMessage = '''async function sendMessage() {
    if (!currentConvId) return;
    const input = document.getElementById("user-input");
    const text = input.value.trim();
    if (!text) return;
    input.value = "";
    input.disabled = true;
    document.getElementById("send-btn").disabled = true;
    clearAutoTimer();
    showTyping(true);

    const box = document.getElementById("chat-box");
    const welcome = document.getElementById("welcome");
    if (welcome) welcome.remove();
    const conv = conversations.find(c => c.id === currentConvId);

    // 用户消息
    box.insertAdjacentHTML("beforeend",
        '<div class="msg-row user">'
        + '<div class="msg-avatar"><img src="' + AVATAR_URL + '" alt=""></div>'
        + '<div class="msg-bubble">' + escapeHtml(text) + '</div>'
        + '</div>');
    box.scrollTop = box.scrollHeight;

    let aiText = "";
    try {
        const res = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ conv_id: currentConvId, message: text })
        });
        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            const chunk = decoder.decode(value);
            const sseLines = chunk.split("\\n");
            for (const sseLine of sseLines) {
                if (!sseLine.startsWith("data: ")) continue;
                const dataStr = sseLine.slice(6);
                if (dataStr === "[DONE]") continue;
                try {
                    const data = JSON.parse(dataStr);
                    if (data.done) {
                        if (conv) {
                            conv.messages = conv.messages || [];
                            conv.messages.push({ role: "user", content: text });
                            conv.messages.push({ role: "assistant", content: data.full });
                        }
                        const lines = data.full.split(/\\n/).filter(l => l.trim());
                        if (lines.length === 0) {
                            showTyping(false);
                            enableInput();
                        } else {
                            showLines(lines, 0);
                        }
                        resetAutoTimer();
                    } else if (data.content) {
                        aiText += data.content;
                    }
                } catch (e) {}
            }
        }
    } catch (err) {
        showTyping(false);
        enableInput();
    }

    function showLines(lines, idx) {
        if (idx >= lines.length) {
            showTyping(false);
            enableInput();
            return;
        }
        const row = document.createElement("div");
        row.className = "msg-row ai";
        row.innerHTML = '<div class="msg-avatar"><img src="/static/ima.jpg" alt=""></div><div class="msg-bubble">' + escapeHtml(lines[idx]) + '</div>';
        box.appendChild(row);
        box.scrollTop = box.scrollHeight;
        setTimeout(function() { showLines(lines, idx + 1); }, 2000);
    }

    function enableInput() {
        input.disabled = false;
        updateSendBtn();
        input.focus();
    }
}'''

content = content[:start] + new_sendMessage + '\n' + content[end:]

with open(r'C:\Users\Encounter\Desktop\chat-app\templates\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('SUCCESS: sendMessage replaced with simple version')
