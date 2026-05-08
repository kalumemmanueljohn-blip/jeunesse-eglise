// static/chat/js/chat.js
// Application de messagerie temps réel

class ChatWebSocket {
    constructor() {
        this.socket = null;
        this.isConnected = false;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 10;
        this.reconnectDelay = 3000;
        this.messageQueue = [];
        this.eventHandlers = {};
    }

    connect() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/chat/`;
        
        this.socket = new WebSocket(wsUrl);
        
        this.socket.onopen = () => {
            console.log('🔌 WebSocket connecté');
            this.isConnected = true;
            this.reconnectAttempts = 0;
            this.flushMessageQueue();
            this.dispatchEvent('connected', {});
        };
        
        this.socket.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                this.handleMessage(data);
            } catch (e) {
                console.error('Erreur de parsing message:', e);
            }
        };
        
        this.socket.onclose = () => {
            console.log('🔌 WebSocket déconnecté');
            this.isConnected = false;
            this.dispatchEvent('disconnected', {});
            this.reconnect();
        };
        
        this.socket.onerror = (error) => {
            console.error('WebSocket erreur:', error);
            this.dispatchEvent('error', error);
        };
    }
    
    reconnect() {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            console.log('Maximum de tentatives de reconnexion atteint');
            this.dispatchEvent('reconnect_failed', {});
            return;
        }
        
        this.reconnectAttempts++;
        console.log(`Tentative de reconnexion ${this.reconnectAttempts}/${this.maxReconnectAttempts} dans ${this.reconnectDelay}ms`);
        
        setTimeout(() => {
            this.connect();
        }, this.reconnectDelay);
    }
    
    send(data) {
        if (this.isConnected && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify(data));
        } else {
            this.messageQueue.push(data);
        }
    }
    
    flushMessageQueue() {
        while (this.messageQueue.length > 0) {
            const data = this.messageQueue.shift();
            this.send(data);
        }
    }
    
    handleMessage(data) {
        switch (data.type) {
            case 'message':
                this.dispatchEvent('new_message', data.data);
                break;
            case 'message_sent':
                this.dispatchEvent('message_sent', data.message);
                break;
            case 'typing':
                this.dispatchEvent('typing', data.data);
                break;
            case 'read':
                this.dispatchEvent('messages_read', data.data);
                break;
            case 'online_status':
                this.dispatchEvent('online_status', data.data);
                break;
            default:
                console.log('Message non géré:', data);
        }
    }
    
    sendMessage(conversationId, content, fileUrl = null, fileName = null) {
        this.send({
            type: 'message',
            conversation_id: conversationId,
            content: content,
            file_url: fileUrl,
            file_name: fileName
        });
    }
    
    sendTyping(conversationId, isTyping) {
        this.send({
            type: 'typing',
            conversation_id: conversationId,
            is_typing: isTyping
        });
    }
    
    markAsRead(messageIds) {
        this.send({
            type: 'read',
            message_ids: messageIds
        });
    }
    
    updateOnlineStatus(isOnline) {
        this.send({
            type: 'online_status',
            is_online: isOnline
        });
    }
    
    on(event, callback) {
        if (!this.eventHandlers[event]) {
            this.eventHandlers[event] = [];
        }
        this.eventHandlers[event].push(callback);
    }
    
    off(event, callback) {
        if (this.eventHandlers[event]) {
            this.eventHandlers[event] = this.eventHandlers[event].filter(cb => cb !== callback);
        }
    }
    
    dispatchEvent(event, data) {
        if (this.eventHandlers[event]) {
            this.eventHandlers[event].forEach(callback => callback(data));
        }
    }
}

// Gestionnaire de messages principal
class ChatManager {
    constructor() {
        this.ws = null;
        this.currentConversationId = null;
        this.userId = null;
        this.typingTimeout = null;
        this.unreadCount = 0;
        this.messageCache = new Map();
    }
    
    init(userId) {
        this.userId = userId;
        this.ws = new ChatWebSocket();
        this.ws.connect();
        
        this.ws.on('new_message', (data) => {
            this.handleNewMessage(data);
        });
        
        this.ws.on('message_sent', (data) => {
            this.handleMessageSent(data);
        });
        
        this.ws.on('typing', (data) => {
            this.handleTypingIndicator(data);
        });
        
        this.ws.on('messages_read', (data) => {
            this.handleMessagesRead(data);
        });
        
        // Mettre à jour le statut en ligne périodiquement
        setInterval(() => {
            if (this.ws.isConnected) {
                this.ws.updateOnlineStatus(true);
            }
        }, 30000);
        
        // Gestion de la visibilité de la page
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden && this.ws.isConnected) {
                this.ws.updateOnlineStatus(true);
            }
        });
    }
    
    setCurrentConversation(conversationId) {
        this.currentConversationId = conversationId;
    }
    
    handleNewMessage(data) {
        if (data.conversation_id === this.currentConversationId) {
            this.appendMessageToUI(data);
            // Marquer comme lu immédiatement
            this.ws.markAsRead([data.id]);
        } else {
            this.updateUnreadBadge(data.conversation_id);
            this.showNotification(data);
        }
        
        // Mettre à jour la liste des conversations
        this.updateConversationPreview(data);
    }
    
    handleMessageSent(data) {
        // Message déjà ajouté via la réponse AJAX
        console.log('Message envoyé:', data);
    }
    
    handleTypingIndicator(data) {
        if (data.conversation_id === this.currentConversationId && data.user_id !== this.userId) {
            this.showTypingIndicator(data.user_name, data.is_typing);
        }
    }
    
    handleMessagesRead(data) {
        if (data.conversation_id === this.currentConversationId) {
            this.updateReadStatus(data.message_ids);
        }
    }
    
    appendMessageToUI(message) {
        // Cette méthode doit être surchargée par la page
        if (window.appendMessageToChat) {
            window.appendMessageToChat(message);
        }
    }
    
    showTypingIndicator(userName, isTyping) {
        if (window.showTyping) {
            window.showTyping(userName, isTyping);
        }
    }
    
    updateReadStatus(messageIds) {
        if (window.markMessagesAsRead) {
            window.markMessagesAsRead(messageIds);
        }
    }
    
    updateUnreadBadge(conversationId) {
        const badge = document.querySelector(`.conversation-item[data-conv-id="${conversationId}"] .unread-badge`);
        if (badge) {
            let count = parseInt(badge.textContent) || 0;
            count++;
            badge.textContent = count;
            badge.style.display = 'inline-flex';
        }
        
        // Mettre à jour le badge global
        const globalBadge = document.querySelector('.badge-messages');
        if (globalBadge) {
            let total = parseInt(globalBadge.textContent) || 0;
            total++;
            globalBadge.textContent = total;
        }
    }
    
    updateConversationPreview(message) {
        const convItem = document.querySelector(`.conversation-item[data-conv-id="${message.conversation_id}"]`);
        if (convItem) {
            const previewSpan = convItem.querySelector('.conversation-preview');
            if (previewSpan) {
                const content = message.content || '[Fichier]';
                const preview = content.length > 35 ? content.substring(0, 35) + '...' : content;
                previewSpan.innerHTML = `<span class="you-label">${message.sender_id === this.userId ? 'Vous: ' : ''}</span>${preview}`;
            }
            
            const timeSpan = convItem.querySelector('.conversation-time');
            if (timeSpan) {
                timeSpan.textContent = this.formatTime(new Date());
            }
            
            // Remonter la conversation en haut
            const parent = convItem.parentNode;
            parent.insertBefore(convItem, parent.firstChild);
        }
    }
    
    showNotification(message) {
        if (document.hidden && Notification.permission === 'granted') {
            new Notification('Nouveau message', {
                body: `${message.sender_name}: ${message.content || 'Fichier envoyé'}`,
                icon: '/static/chat/images/chat-icon.png',
                tag: message.conversation_id
            });
        }
    }
    
    formatTime(date) {
        const hours = date.getHours().toString().padStart(2, '0');
        const minutes = date.getMinutes().toString().padStart(2, '0');
        return `${hours}:${minutes}`;
    }
    
    requestNotificationPermission() {
        if ('Notification' in window && Notification.permission !== 'granted' && Notification.permission !== 'denied') {
            Notification.requestPermission();
        }
    }
}

// Utilitaires pour le chat
const ChatUtils = {
    // Échapper le HTML
    escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },
    
    // Formater la taille du fichier
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },
    
    // Obtenir le type de fichier à partir de l'extension
    getFileType(filename) {
        if (!filename) return 'file';
        const ext = filename.split('.').pop().toLowerCase();
        const imageExts = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp', 'svg'];
        const videoExts = ['mp4', 'mov', 'avi', 'mkv', 'webm'];
        const audioExts = ['mp3', 'wav', 'ogg', 'm4a'];
        const pdfExts = ['pdf'];
        const docExts = ['doc', 'docx', 'txt', 'rtf'];
        
        if (imageExts.includes(ext)) return 'image';
        if (videoExts.includes(ext)) return 'video';
        if (audioExts.includes(ext)) return 'audio';
        if (pdfExts.includes(ext)) return 'pdf';
        if (docExts.includes(ext)) return 'document';
        return 'file';
    },
    
    // Obtenir l'icône pour un type de fichier
    getFileIcon(fileType) {
        const icons = {
            image: 'bi bi-image',
            video: 'bi bi-camera-reels',
            audio: 'bi bi-music-note',
            pdf: 'bi bi-file-pdf',
            document: 'bi bi-file-text',
            file: 'bi bi-paperclip'
        };
        return icons[fileType] || icons.file;
    },
    
    // Scroll en bas d'un élément
    scrollToBottom(element) {
        if (element) {
            element.scrollTop = element.scrollHeight;
        }
    },
    
    // Créer un élément DOM
    createElement(tag, className, innerHtml = '') {
        const el = document.createElement(tag);
        if (className) el.className = className;
        if (innerHtml) el.innerHTML = innerHtml;
        return el;
    },
    
    // Obtenir le cookie CSRF
    getCsrfToken() {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, 10) === 'csrftoken=') {
                    cookieValue = decodeURIComponent(cookie.substring(10));
                    break;
                }
            }
        }
        return cookieValue;
    },
    
    // Debounce pour limiter les appels
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Formater la date relative
    timeAgo(date) {
        const now = new Date();
        const diff = now - date;
        
        const seconds = Math.floor(diff / 1000);
        const minutes = Math.floor(seconds / 60);
        const hours = Math.floor(minutes / 60);
        const days = Math.floor(hours / 24);
        
        if (days > 30) {
            return date.toLocaleDateString();
        } else if (days > 0) {
            return `${days}j`;
        } else if (hours > 0) {
            return `${hours}h`;
        } else if (minutes > 0) {
            return `${minutes}m`;
        } else {
            return "à l'instant";
        }
    },
    
    // Sauvegarder des données dans sessionStorage
    saveToSession(key, value) {
        try {
            sessionStorage.setItem(`chat_${key}`, JSON.stringify(value));
        } catch (e) {
            console.error('Erreur saveToSession:', e);
        }
    },
    
    // Charger des données depuis sessionStorage
    loadFromSession(key) {
        try {
            const data = sessionStorage.getItem(`chat_${key}`);
            return data ? JSON.parse(data) : null;
        } catch (e) {
            console.error('Erreur loadFromSession:', e);
            return null;
        }
    },
    
    // Supprimer des données de session
    clearSession(key) {
        sessionStorage.removeItem(`chat_${key}`);
    }
};

// Initialisation globale
window.ChatWebSocket = ChatWebSocket;
window.ChatManager = ChatManager;
window.ChatUtils = ChatUtils;

// Initialiser le gestionnaire de chat quand le DOM est prêt
let chatManager = null;

document.addEventListener('DOMContentLoaded', () => {
    // Récupérer l'ID utilisateur depuis un attribut data sur le body
    const userId = document.body.dataset.userId;
    if (userId && !chatManager) {
        chatManager = new ChatManager();
        chatManager.init(parseInt(userId));
        window.chatManager = chatManager;
        
        // Demander la permission pour les notifications
        if (Notification.permission !== 'granted' && Notification.permission !== 'denied') {
            setTimeout(() => {
                chatManager.requestNotificationPermission();
            }, 5000);
        }
    }
});

// Export pour les modules (si utilisé avec des modules)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ChatWebSocket, ChatManager, ChatUtils };
}