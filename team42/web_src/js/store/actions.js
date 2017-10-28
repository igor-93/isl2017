/**
 * Created by raphi on 27.03.2017.
 */
import {ENDPOINTS} from '../webSocketUtils';

export const ACTION_TYPES = {
  SET_WEB_SOCKET_BRIDGE: "SET_WEB_SOCKET_BRIDGE",
  SET_WEB_SOCKET_STATE: "SET_WEB_SOCKET_STATE",
  GET_POSTS_OVERVIEW: "GET_POSTS_OVERVIEW",
  GET_USER_PROFILE: "GET_USER_PROFILE",
  GET_USER_POSTS: "GET_USER_POSTS",
  SEARCH_USERS: "SEARCH_USERS",
  TRACK_USER: "TRACK_USER",
  UNTRACK_USER: "UNTRACK_USER",
  GET_TRACKED_USERS: "GET_TRACKED_USERS",
  GET_TRACKING_DATA: "GET_TRACKING_DATA",
  GET_TRACKING_DATA_AGGREGATED: "GET_TRACKING_DATA_AGGREGATED",
  UPDATE_TRACKING_DATA: "UPDATE_TRACKING_DATA",
  UPDATE_FOLLOWING_DATA: "UPDATE_FOLLOWING_DATA",
  GET_POST_COMMENTS: "GET_POST_COMMENTS",
  GET_UNFOLLOWING_USERS: "GET_UNFOLLOWING_USERS",
  GET_RECENT_COMMENTS: "GET_RECENT_COMMENTS",
  GET_POST_EMOJIS: "GET_POST_EMOJIS",
  _RECEIVED: "_RECEIVED",
  _SENT: "_SENT"
};

function sendType(type) {
    return type + ACTION_TYPES._SENT;
}

function receiveType(type) {
    return type + ACTION_TYPES._RECEIVED;
}

function action(type) {
    return {type: type};
}

export function setWebSocketStateAction(connected) {
    return {type: ACTION_TYPES.SET_WEB_SOCKET_STATE, connected: connected}
}

export function setWebSocketBridgeAction(webSocketBridge) {
    return {type: ACTION_TYPES.SET_WEB_SOCKET_BRIDGE, webSocketBridge: webSocketBridge}
}

export function receiveMessage(msg) {
    return (dispatch, getState) => {
        dispatch(receiveMessageAction(msg));
        switch (msg.action) {
            case ACTION_TYPES.TRACK_USER:
                dispatch(fetchAggregatedTrackingData());
                break;
            case ACTION_TYPES.UNTRACK_USER:
                dispatch(fetchAggregatedTrackingData());
                break;
            default:
                break;
        }
    };
}

export function receiveMessageAction(msg) {
    return Object.assign(msg, {type: receiveType(msg.action)})
}

export function fetchUserProfile() {
    return (dispatch, getState) => {
        const {webSocketBridge, webSocketConnected} = getState();
        dispatch(action(sendType(ACTION_TYPES.GET_USER_PROFILE)));
        webSocketBridge.stream(ENDPOINTS.USER).send({action: ACTION_TYPES.GET_USER_PROFILE});
    };
}

export function fetchUserPosts(fetchNext = false) {
    return (dispatch, getState) => {
        const {webSocketBridge, webSocketConnected, postsStatus} = getState();
        dispatch(action(sendType(ACTION_TYPES.GET_USER_POSTS)));
        let nextCursor = 1;
        if (fetchNext) {
            nextCursor = postsStatus.nextCursor;
        }
        webSocketBridge.stream(ENDPOINTS.POSTS).send({action: ACTION_TYPES.GET_USER_POSTS, cursor: nextCursor});
    };
}

export function fetchPostComments(post, fetchNext = false) {
        return (dispatch, getState) => {
        const {webSocketBridge, webSocketConnected} = getState();
        dispatch({type: sendType(ACTION_TYPES.GET_POST_COMMENTS), postcode: post.code});
        let nextCursor = 1;
        if (fetchNext) {
            nextCursor = post._comments_nextCursor || 1;
        }
        webSocketBridge.stream(ENDPOINTS.POSTS).send({action: ACTION_TYPES.GET_POST_COMMENTS, cursor: nextCursor, postcode: post.code});
    };
}

export function fetchUserSearchResults(queryString) {
    const queryValue = queryString.replace(/\s/g, "+");
    return (dispatch, getState) => {
        const {webSocketBridge, webSocketConnected} = getState();
        dispatch(action(sendType(ACTION_TYPES.SEARCH_USERS)));
        webSocketBridge.stream(ENDPOINTS.USER).send({action: ACTION_TYPES.SEARCH_USERS, query: queryValue});
    };
}

export function trackUser(username) {
    return (dispatch, getState) => {
        const {webSocketBridge, webSocketConnected} = getState();
        dispatch(action(sendType(ACTION_TYPES.TRACK_USER)));
        webSocketBridge.stream(ENDPOINTS.USER).send({action: ACTION_TYPES.TRACK_USER, instagram_username: username});
    };
}

export function untrackUser(username) {
    return (dispatch, getState) => {
        const {webSocketBridge, webSocketConnected} = getState();
        dispatch(action(sendType(ACTION_TYPES.UNTRACK_USER)));
        webSocketBridge.stream(ENDPOINTS.USER).send({action: ACTION_TYPES.UNTRACK_USER, instagram_username: username});
    };
}

export function fetchTrackedUsers() {
    return (dispatch, getState) => {
        const {webSocketBridge, webSocketConnected} = getState();
        dispatch(action(sendType(ACTION_TYPES.GET_TRACKED_USERS)));
        webSocketBridge.stream(ENDPOINTS.USER).send({action: ACTION_TYPES.GET_TRACKED_USERS});
    };
}

export function fetchTrackingData(username) {
    return (dispatch, getState) => {
        const {webSocketBridge, webSocketConnected} = getState();
        dispatch(action(sendType(ACTION_TYPES.GET_TRACKING_DATA)));
        webSocketBridge.stream(ENDPOINTS.USER).send({action: ACTION_TYPES.GET_TRACKING_DATA, instagram_username: username});
    };
}

export function fetchAggregatedTrackingData() {
    return (dispatch, getState) => {
        const {webSocketBridge, webSocketConnected} = getState();
        dispatch(action(sendType(ACTION_TYPES.GET_TRACKING_DATA_AGGREGATED)));
        webSocketBridge.stream(ENDPOINTS.USER).send({action: ACTION_TYPES.GET_TRACKING_DATA_AGGREGATED});
    };
}

export function fetchUnfollowingUsers() {
    return (dispatch, getState) => {
        const {webSocketBridge, webSocketConnected} = getState();
        dispatch(action(sendType(ACTION_TYPES.GET_UNFOLLOWING_USERS)));
        webSocketBridge.stream(ENDPOINTS.USER).send({action: ACTION_TYPES.GET_UNFOLLOWING_USERS});
    };
}

export function updateTrackingData() {
    return (dispatch, getState) => {
        const {webSocketBridge, webSocketConnected} = getState();
        dispatch(action(sendType(ACTION_TYPES.UPDATE_TRACKING_DATA)));
        webSocketBridge.stream(ENDPOINTS.USER).send({action: ACTION_TYPES.UPDATE_TRACKING_DATA});
    };
}

export function updateFollowingData() {
    return (dispatch, getState) => {
        const {webSocketBridge, webSocketConnected} = getState();
        dispatch(action(sendType(ACTION_TYPES.UPDATE_FOLLOWING_DATA)));
        webSocketBridge.stream(ENDPOINTS.USER).send({action: ACTION_TYPES.UPDATE_FOLLOWING_DATA});
    };
}

export function fetchRecentComments(first = false) {
    return (dispatch, getState) => {
        const {webSocketBridge, commentsStatus} = getState();
        dispatch(action(sendType(ACTION_TYPES.GET_RECENT_COMMENTS)));
        webSocketBridge.stream(ENDPOINTS.POSTS).send({
            action: ACTION_TYPES.GET_RECENT_COMMENTS,
            from_ts: first || !commentsStatus.oldest_ts ? null : (commentsStatus.oldest_ts - 1)
        });
    };
}

export function fetchPostEmojis(postcode) {
        return (dispatch, getState) => {
        const {webSocketBridge, commentsStatus} = getState();
        dispatch({postcode: postcode, type: sendType(ACTION_TYPES.GET_POST_EMOJIS)});
        webSocketBridge.stream(ENDPOINTS.POSTS).send({
            postcode: postcode,
            action: ACTION_TYPES.GET_POST_EMOJIS
        });
    };
}



