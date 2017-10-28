/**
 * Created by raphi on 18.03.2017.
 */
import {APP_INIT} from '../constants';
import { createStore, applyMiddleware, compose } from 'redux';
import thunk from 'redux-thunk';
import rootReducer from './reducers';

export function initStore() {
    const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
    return createStore(
        rootReducer,
        composeEnhancers(applyMiddleware(thunk))
    );
}

export function getInitArray() {
    return [
        APP_INIT.WEB_SOCKET
    ];
}