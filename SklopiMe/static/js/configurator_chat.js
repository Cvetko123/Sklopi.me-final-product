// Marko Ciric 2023/0133
// Aleksandar Raskovic - dodao restore chat history
(function () {
    'use strict';

    function getCookie(name) {
        const match = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
        return match ? decodeURIComponent(match.pop()) : '';
    }

    const csrftoken = getCookie('csrftoken');
    const chatHistory = document.getElementById('chat-history');
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('chat-send-btn');

    const activeComponentIds = new Set();
    const idInputs = document.querySelectorAll('.component-table .active-component-id');
    idInputs.forEach(function (input) {
        const idVal = input.value;
        if (idVal) {
            activeComponentIds.add(parseInt(idVal, 10));
        }
    });

    function appendMessage(text, cssClass) {
        const el = document.createElement('div');
        el.className = 'message ' + cssClass;
        el.textContent = text;
        chatHistory.appendChild(el);
        chatHistory.scrollTop = chatHistory.scrollHeight;
        return el;
    }

    function buildRecommendationCard(item) {
        const card = document.createElement('div');
        card.className = 'rec-card';
        card.innerHTML =
            '<span class="rec-name"></span>' +
            '<span class="rec-price"></span>' +
            '<button class="rec-add" type="button">Dodaj</button>';

        card.querySelector('.rec-name').textContent = item.name;
        card.querySelector('.rec-price').textContent = item.price_display;

        const addBtn = card.querySelector('.rec-add');
        if (activeComponentIds.has(item.id)) {
            addBtn.disabled = true;
            addBtn.textContent = 'Dodato ✓';
        }
        addBtn.addEventListener('click', function () {
            addComponentToBuild(item, addBtn);
        });

        return card;
    }

    function appendRecommendations(recommendations) {
        const wrapper = document.createElement('div');
        wrapper.className = 'message ai-message';

        const container = document.createElement('div');
        container.className = 'ai-recommendations';
        recommendations.forEach(function (item) {
            container.appendChild(buildRecommendationCard(item));
        });

        wrapper.appendChild(container);
        chatHistory.appendChild(wrapper);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    function appendRecommendationsByCategory(byCategory) {
        const wrapper = document.createElement('div');
        wrapper.className = 'message ai-message';

        Object.keys(byCategory).forEach(function (componentType) {
            const items = byCategory[componentType];
            if (!items.length) return;

            const heading = document.createElement('div');
            heading.className = 'ai-recommendations-heading';
            heading.textContent = componentType.toUpperCase();
            wrapper.appendChild(heading);

            const container = document.createElement('div');
            container.className = 'ai-recommendations';
            items.forEach(function (item) {
                container.appendChild(buildRecommendationCard(item));
            });
            wrapper.appendChild(container);
        });

        chatHistory.appendChild(wrapper);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    function sendChatMessage() {
        const text = chatInput.value.trim();
        if (!text) return;

        appendMessage(text, 'user-message');
        chatInput.value = '';
        sendBtn.disabled = true;

        fetch(window.CONFIGURATOR_CHAT_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ message: text }),
        })
            .then(function (response) {
                return response.json().then(function (data) {
                    return { ok: response.ok, data: data };
                });
            })
            .then(function (result) {
                const data = result.data;

                if (!result.ok && !data.message) {
                    appendMessage('Došlo je do neočekivane greške. Pokušajte ponovo.', 'ai-message error');
                    return;
                }

                appendMessage(data.message, 'ai-message');

                if (data.recommendations && data.recommendations.length) {
                    appendRecommendations(data.recommendations);
                } else if (data.recommendations_by_category) {
                    appendRecommendationsByCategory(data.recommendations_by_category);
                }
            })
            .catch(function () {
                appendMessage('Nije moguće kontaktirati server. Proverite konekciju i pokušajte ponovo.', 'ai-message error');
            })
            .finally(function () {
                sendBtn.disabled = false;
            });
    }

    function addComponentToBuild(item, buttonEl) {
        buttonEl.disabled = true;
        buttonEl.textContent = 'Dodavanje...';

        fetch(window.CONFIGURATOR_ADD_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                component_type: item.component_type,
                component_id: item.id,
            }),
        })
            .then(function (response) {
                return response.json().then(function (data) {
                    return { ok: response.ok, data: data };
                });
            })
            .then(function (result) {
                if (!result.ok) {
                    buttonEl.disabled = false;
                    buttonEl.textContent = 'Dodaj';
                    appendMessage(result.data.error || 'Komponentu nije moguće dodati.', 'ai-message error');
                    return;
                }
                buttonEl.textContent = 'Dodato ✓';
                setTimeout(function () {
                    window.location.reload();
                }, 400);
            })
            .catch(function () {
                buttonEl.disabled = false;
                buttonEl.textContent = 'Dodaj';
                appendMessage('Nije moguće kontaktirati server. Pokušajte ponovo.', 'ai-message error');
            });
    }

    sendBtn.addEventListener('click', sendChatMessage);
    chatInput.addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            sendChatMessage();
        }
    });
    const historyScript = document.getElementById('chat-history-data');
    if (historyScript) {
        try {
            const history = JSON.parse(historyScript.textContent);
            if (Array.isArray(history)) {
                history.forEach(function (chat) {
                    if (chat.sender === 'user') {
                        appendMessage(chat.message, 'user-message');
                    } else if (chat.sender === 'ai') {
                        let cssClass = 'ai-message';
                        if (chat.status === 'invalid_request' || chat.status === 'no_results') {
                            cssClass += ' error';
                        }

                        appendMessage(chat.message, cssClass);


                        if (chat.recommendations && chat.recommendations.length) {
                            appendRecommendations(chat.recommendations);
                        } else if (chat.recommendations_by_category) {
                            appendRecommendationsByCategory(chat.recommendations_by_category);
                        }
                    }
                });
            }
        } catch (e) {
            console.error('Greška pri učitavanju istorije ćaskanja:', e);
        }
    }
})();