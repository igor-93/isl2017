import {setWebSocketStateAction, setWebSocketBridgeAction, receiveMessage} from './store/actions';
import {WebSocketBridge} from 'django-channels';

export const ENDPOINTS = {
    POSTS: "POSTS",
    USER: "USER"
};

export function initWebSockets(store) {
    const socketBridge = new WebSocketBridge({
        onopen: () => {
            store.dispatch(setWebSocketStateAction(true));
        }
    });
    store.dispatch(setWebSocketBridgeAction(socketBridge));
    socketBridge.connect("ws://" + window.location.host + "/app");
    socketBridge.listen();
    Object.keys(ENDPOINTS).forEach((key) => {
        socketBridge.demultiplex(ENDPOINTS[key], (action, stream) => {
            store.dispatch(receiveMessage(action))
        });
    });
}