import { process } from '/env.js';
import { Configuration, OpenAIApi } from 'openai';

const apiKey = process.env.OPENAI_API_KEY;

if (!apiKey) {
    console.error('API key is missing. Please set the OPENAI_API_KEY environment variable.');
    process.exit(1);
}

console.log('API key:', apiKey);

const configuration = new Configuration({
    apiKey: apiKey
});

delete configuration.baseOptions.headers['User-Agent'];

const openai = new OpenAIApi(configuration);

const conversationArr = [
    { 
        role: 'system',
        content: 'You are a useful assistant.'
    }
];

const chatbotConversation = document.getElementById('chatbot-conversation');

document.addEventListener('submit', (e) => {
    e.preventDefault();
    const userInput = document.getElementById('user-input');
    const newSpeechBubble = document.createElement('div');
    newSpeechBubble.classList.add('speech', 'speech-human');
    chatbotConversation.appendChild(newSpeechBubble);
    newSpeechBubble.textContent = userInput.value;
    
    conversationArr.push({ 
        role: 'user',
        content: userInput.value
    });
    
    userInput.value = '';
    chatbotConversation.scrollTop = chatbotConversation.scrollHeight;
    fetchReply();
});

async function fetchReply(){
    try {
        const response = await openai.createChatCompletion({
            model: 'gpt-4o-mini',
            messages: conversationArr,
        });
        conversationArr.push(response.data.choices[0].message);
        renderTypewriterText(response.data.choices[0].message.content);
    } catch (error) {
        console.error('Error fetching reply:', error);
    }
}

function renderTypewriterText(text) {
    const newSpeechBubble = document.createElement('div');
    newSpeechBubble.classList.add('speech', 'speech-bot');
    chatbotConversation.appendChild(newSpeechBubble);
    newSpeechBubble.textContent = text;
}