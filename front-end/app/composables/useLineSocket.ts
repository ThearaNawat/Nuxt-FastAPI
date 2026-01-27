export type LineMessage = {
    user_id: string;
    group_id: string | null;
    user_name: string;
    group_name: string | null;
    question: string;
    answer: string;
    date_time: string | Date | null;
    chat_type: string | null;
};

export function useLineSocket() {
    const messages = ref<LineMessage[]>([]);
    const socket = ref<WebSocket | null>(null);
    const connected = ref(false);

    const connect = () => {
        socket.value = new WebSocket(`ws://localhost:8000/linebot`);

        socket.value.onopen = () => {
            connected.value = true;
            console.log('WebSocket connected');
        };

        socket.value.onmessage = (event) => {
            const data = JSON.parse(event.data) as LineMessage;
            messages.value.push(data);
            console.log('All messages:', messages.value);
        };

        socket.value.onclose = () => {
            connected.value = false;
            console.log('WebSocket disconnected');
        };
    }

    const disconnect = () => {
        socket.value?.close();
    }
    // onMounted(connect);
    // onUnmounted(disconnect);

    return {
        messages,
        connected,
        connect,
        disconnect,
        socket
    }
}