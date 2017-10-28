/**
 * Created by raphi on 18.03.2017.
 */
import {combineReducers} from 'redux';
import {ACTION_TYPES, sendAction, receiveAction} from './actions';
import {APP_STATE, APP_INIT, FETCH_STATUS} from '../constants';
import {getInitArray} from './storeUtils';

/*HELPERS*/

const emptyReducer = (state = null, action) => state;

function createReducer(initialState, handlers) {
    return function reducer(state = initialState, action) {
        if (handlers.hasOwnProperty(action.type)) {
            return handlers[action.type](state, action)
        } else {
            return state
        }
    }
}

function wrapGlobalReducer(reducer, globalState, oldState) {
    return (state, action) => reducer(state, action, globalState, oldState);
}

function updateObject(oldObject, newValues) {
    return Object.assign({}, oldObject, newValues);
}

function arrayToMap(array = [], key = 'id') {
    const map = {};
    array.forEach((element) => {
       map[element[key]] = element;
    });
    return map;
}

function updateItemInArray(array, itemId, updateItemCallback) {
    return array.map(item => {
        if (item.id !== itemId) {
            // Since we only want to update one item, preserve all others as they are now
            return item;
        }

        // Use the provided callback to create an updated item
        const updatedItem = updateItemCallback(item);
        return updatedItem;
    });
}

function updatePost(oldPost, newData = {}) {
    const newComments = newData.comments || [];
    let mergedComments =  oldPost.comments.concat(newComments);
    mergedComments = Array.from(new Set(mergedComments));
    return Object.assign({}, oldPost, newData, {comments: mergedComments});
}

function updateTable(oldTable, newData = {}, elementUpdateFunc) {
    let updateFunc = elementUpdateFunc;
    if (!(typeof updateFunc === 'function')) {
        return Object.assign({}, oldTable, newData);
    }
    const updates = {};
    Object.keys(newData).forEach((key) => {
       if (oldTable[key]) {
           updates[key] = updateFunc(oldTable[key], newData[key]);
       }
    });
    return Object.assign({},oldTable, newData, updates);
}

/*REDUCERS*/
/**
 * Reducer which handles state during initialization
 */
const appInitReducer = createReducer(getInitArray(), {
    [ACTION_TYPES.SET_WEB_SOCKET_STATE]: (state, action) => {
        return state.filter((el) => el !== APP_INIT.WEB_SOCKET);
    }
});

/**
 * Reducer for user data
 */
const userReducer = createReducer({}, {
    [ACTION_TYPES.GET_USER_PROFILE + ACTION_TYPES._RECEIVED]: (state, action) => {
        return updateObject(state, action.user)
    },
});

/**
 * Reducer for user data status
 */
const userStatusReducer = createReducer({fetchStatus: null}, {
    [ACTION_TYPES.GET_USER_PROFILE + ACTION_TYPES._SENT]: (state, action) => {
        return updateObject(state, {fetchStatus: FETCH_STATUS.FETCHING})
    },
    [ACTION_TYPES.GET_USER_PROFILE + ACTION_TYPES._RECEIVED]: (state, action) => {
        return updateObject(state, {fetchStatus: FETCH_STATUS.SUCCESS})
    }
});

/**
 * Reducer for post list data
 */
const postsReducer = createReducer([], {
    [ACTION_TYPES.GET_USER_POSTS + ACTION_TYPES._RECEIVED]: (state, action) => {
        return state.concat(action.posts);
    },
    [ACTION_TYPES.GET_POST_COMMENTS + ACTION_TYPES._SENT]: (state, action) => {
        const update = {_comments_fetchStatus: FETCH_STATUS.FETCHING};
        return state.map((post) => {
            if (post.code === action.postcode) {
                return Object.assign({}, post, update);
            } else {
                return post;
            }
        });
    },
    [ACTION_TYPES.GET_POST_COMMENTS + ACTION_TYPES._RECEIVED]: (state, action) => {
        const {new_cursor, comments} = action;
        const update = {_comments_nextCursor: new_cursor, _comments_fetchStatus: FETCH_STATUS.SUCCESS};
        return state.map((post) => {
            if (post.code === action.postcode) {
                const newPost = Object.assign({}, post, update);
                if (new_cursor === post._comments_nextCursor) {
                    newPost.comments = comments;
                } else {
                    newPost.comments = post.comments.concat(comments);
                }
                return newPost;
            } else {
                return post;
            }
        });
    },
    [ACTION_TYPES.GET_POST_EMOJIS + ACTION_TYPES._SENT]: (state, action) => {
        const update = {_emoji_fetchStatus: FETCH_STATUS.FETCHING};
        return state.map((post) => {
            if (post.code === action.postcode) {
                return Object.assign({}, post, update);
            } else {
                return post;
            }
        });
    },
    [ACTION_TYPES.GET_POST_EMOJIS + ACTION_TYPES._RECEIVED]: (state, action) => {
        const update = {_emoji_fetchStatus: FETCH_STATUS.SUCCESS, emojis: action.emojis};
        return state.map((post) => {
            if (post.code === action.postcode) {
                return Object.assign({}, post, update);
            } else {
                return post;
            }
        });
    }
});

/**
 * Reducer for post list data status
 */
const postsStatusReducer = createReducer({fetchStatus: null, nextCursor: 1}, {
    [ACTION_TYPES.GET_USER_POSTS + ACTION_TYPES._SENT]: (state, action) => {
        return Object.assign({}, state, {fetchStatus: FETCH_STATUS.FETCHING});
    },
    [ACTION_TYPES.GET_USER_POSTS + ACTION_TYPES._RECEIVED]: (state, action) => {
        return Object.assign({}, state, {fetchStatus: FETCH_STATUS.SUCCESS, nextCursor: action.new_cursor});
    },
});

/**
 * Reducer for websocket state
 */
const webSocketStateReducer = createReducer(false, {
    [ACTION_TYPES.SET_WEB_SOCKET_BRIDGE]: (state, action) => {
        return false;
    },
    [ACTION_TYPES.SET_WEB_SOCKET_STATE]: (state, action) => {
        return action.connected;
    }
});

/**
 * Reducer for websocket object
 */
const webSocketBridgeReducer = (state = null, action) => {
    if (action.type === ACTION_TYPES.SET_WEB_SOCKET_BRIDGE) {
        return action.webSocketBridge;
    } else {
        return state;
    }
};

/**
 * Reduer for user search data
 */
const userSearchResultsReducer = createReducer([], {
    [ACTION_TYPES.SEARCH_USERS + ACTION_TYPES._RECEIVED]: (state, action) => {
        return action.users || [];
    }
});

/**
 * Reducer for user search fetching status
 */
const userSearchStatusReducer = createReducer(null, {
    [ACTION_TYPES.SEARCH_USERS + ACTION_TYPES._RECEIVED]: (state, action) => {
        return FETCH_STATUS.SUCCESS;
    },
    [ACTION_TYPES.SEARCH_USERS + ACTION_TYPES._SENT]: (state, action) => {
        return FETCH_STATUS.FETCHING;
    }
});

/**
 * Reducer for tracked users data
 */
const trackedUsersReducer = createReducer([], {
    [ACTION_TYPES.GET_TRACKED_USERS + ACTION_TYPES._RECEIVED]: (state, action) => {
        return action.users || [];
    },
    [ACTION_TYPES.UPDATE_TRACKING_DATA + ACTION_TYPES._RECEIVED]: (state, action) => {
        return action.users || [];
    },
    [ACTION_TYPES.TRACK_USER + ACTION_TYPES._RECEIVED]: (state, action) => {
        return action.users || [];
    },
    [ACTION_TYPES.UNTRACK_USER + ACTION_TYPES._RECEIVED]: (state, action) => {
        return action.users || [];
    },
    [ACTION_TYPES.GET_TRACKING_DATA + ACTION_TYPES._RECEIVED]: (state, action) => {
        const {best_tags, best_time, _ts} = action;

        var new_best_tags = [];
        var index;
        for (index = 0; index < best_tags.length; ++index) {
            var tag = best_tags[index];
            new_best_tags.push([tag['tag'],tag['score']]);
        }
        const update = {best_tags: new_best_tags, best_time, _details_ts: _ts};
        return state.map((user) => {
            if (user.username === action.instagram_username) {
                return Object.assign({}, user, update);
            } else {
                return user;
            }
        });
    }
});

/**
 * Reducer for tracked user status
 */
const trackedUsersStatusReducer = createReducer({fetchStatus: null, serverUpdate_ts: 0}, {
    [ACTION_TYPES.GET_TRACKED_USERS + ACTION_TYPES._RECEIVED]: (state, action) => {
        return Object.assign({}, state, {fetchStatus: FETCH_STATUS.SUCCESS});
    },
    [ACTION_TYPES.GET_TRACKED_USERS + ACTION_TYPES._SENT]: (state, action) => {
        return Object.assign({}, state, {fetchStatus: FETCH_STATUS.FETCHING});
    },
    [ACTION_TYPES.UPDATE_TRACKING_DATA + ACTION_TYPES._RECEIVED]: (state, action) => {
        return Object.assign({}, state, {fetchStatus: FETCH_STATUS.SUCCESS, serverUpdate_ts: action.update_ts});
    },
    [ACTION_TYPES.UPDATE_TRACKING_DATA + ACTION_TYPES._SENT]: (state, action) => {
        return Object.assign({}, state, {fetchStatus: FETCH_STATUS.FETCHING});
    },
    [ACTION_TYPES.TRACK_USER + ACTION_TYPES._RECEIVED]: (state, action) => {
        return Object.assign({}, state, {fetchStatus: FETCH_STATUS.SUCCESS});
    },
    [ACTION_TYPES.TRACK_USER + ACTION_TYPES._SENT]: (state, action) => {
        return Object.assign({}, state, {fetchStatus: FETCH_STATUS.FETCHING});
    },
    [ACTION_TYPES.UNTRACK_USER + ACTION_TYPES._RECEIVED]: (state, action) => {
        return Object.assign({}, state, {fetchStatus: FETCH_STATUS.SUCCESS});
    },
    [ACTION_TYPES.UNTRACK_USER + ACTION_TYPES._SENT]: (state, action) => {
        return Object.assign({}, state, {fetchStatus: FETCH_STATUS.FETCHING});
    }
});

/**
 * Reducer for aggregated tracking data
 */
const aggregatedTrackingDataReducer = createReducer({}, {
    [ACTION_TYPES.GET_TRACKING_DATA_AGGREGATED + ACTION_TYPES._SENT]: (state, action) => {
        return Object.assign({}, state, {_ts: null});
    },
    [ACTION_TYPES.GET_TRACKING_DATA_AGGREGATED + ACTION_TYPES._RECEIVED]: (state, action) => {
        const {best_tags, best_time, _ts} = action;
        var new_best_tags = [];
        var index;
        for (index = 0; index < best_tags.length; ++index) {
            var tag = best_tags[index];
            new_best_tags.push([tag['tag'],tag['score']]);
        }
        return {best_tags: new_best_tags, best_time, _ts};
    }
});

/**
 * Reducer for unfollowing users data
 */
const unfollowingUsersReducer = createReducer([], {
    [ACTION_TYPES.GET_UNFOLLOWING_USERS + ACTION_TYPES._RECEIVED]: (state, action) => {
        return action.users || [];
    },
    [ACTION_TYPES.UPDATE_FOLLOWING_DATA + ACTION_TYPES._RECEIVED]: (state, action) => {
        return action.users || [];
    }
});

/**
 * Reducer for unfollowing users status
 */
const unfollowingUsersStatusReducer = createReducer({fetchStatus: null, serverUpdate_ts: 0}, {
    [ACTION_TYPES.GET_UNFOLLOWING_USERS + ACTION_TYPES._RECEIVED]: (state, action) => {
        return Object.assign({}, state, {fetchStatus: FETCH_STATUS.SUCCESS});
    },
    [ACTION_TYPES.GET_UNFOLLOWING_USERS + ACTION_TYPES._SENT]: (state, action) => {
        return Object.assign({}, state, {fetchStatus: FETCH_STATUS.FETCHING});
    },
    [ACTION_TYPES.UPDATE_FOLLOWING_DATA + ACTION_TYPES._RECEIVED]: (state, action) => {
        return Object.assign({}, state, {fetchStatus: FETCH_STATUS.SUCCESS, serverUpdate_ts: action.update_ts})
    },
    [ACTION_TYPES.UPDATE_FOLLOWING_DATA + ACTION_TYPES._SENT]: (state, action) => {
        return Object.assign({}, state, {fetchStatus: FETCH_STATUS.FETCHING});
    }
});

/**
 * Reducer for unfollowing users data
 */
const commentsReducer = createReducer([], {
    [ACTION_TYPES.GET_RECENT_COMMENTS + ACTION_TYPES._RECEIVED]: (state, action) => {
        return action.comments;
    }
});

/**
 * Reducer for unfollowing users status
 */
const commentsStatusReducer = createReducer({fetchStatus: null, newest_ts: null, oldest_ts: null}, {
    [ACTION_TYPES.GET_RECENT_COMMENTS + ACTION_TYPES._RECEIVED]: (state, action) => {
        return Object.assign({}, state, {fetchStatus: FETCH_STATUS.SUCCESS, oldest_ts: action.oldestComment_ts});
    },
    [ACTION_TYPES.GET_RECENT_COMMENTS + ACTION_TYPES._SENT]: (state, action) => {
        return Object.assign({}, state, {fetchStatus: FETCH_STATUS.FETCHING});
    },
});

/**
 * Reducer for comment data [tabled]
 */
const commentTableReducer = createReducer({}, {
    [ACTION_TYPES.GET_RECENT_COMMENTS + ACTION_TYPES._RECEIVED]: (state, action) => {
        const newTable = {};
        action.comments.forEach((comment) => {
           newTable[comment.id] = comment;
        });
        return updateTable(state, newTable);
    },
    [ACTION_TYPES.GET_POST_COMMENTS + ACTION_TYPES._RECEIVED]: (state, action) => {
        return updateTable(state, arrayToMap(action.comments));
    }
});


/**
 * Reducer for post data [tabled]
 */
const postTableReducer = createReducer({}, {
    [ACTION_TYPES.GET_RECENT_COMMENTS + ACTION_TYPES._RECEIVED]: (state, action) => {
        const newTable = action.postsMap;
        return updateTable(state, newTable, updatePost);
    },
    [ACTION_TYPES.GET_USER_POSTS + ACTION_TYPES._RECEIVED]: (state, action) => {
        const postMap = {};
        action.posts.forEach((post) => {
            post.comments = [];
            postMap[post.code] = post;
        });
        return updateTable(state, postMap, updatePost);
    },
    [ACTION_TYPES.GET_POST_COMMENTS + ACTION_TYPES._SENT]: (state, action) => {
        const {postcode} = action;
        const newTable = updateTable(state);
        newTable[postcode] = updatePost(newTable[postcode], {_comments_fetchStatus: FETCH_STATUS.FETCHING});
        return newTable;
    },

    [ACTION_TYPES.GET_POST_COMMENTS + ACTION_TYPES._RECEIVED]: (state, action) => {
        const {new_cursor, comments, postcode} = action;
        const newTable = updateTable(state);
        const commentIds = comments.map((comment) => comment.id);
        newTable[postcode] = updatePost(newTable[postcode], {
            comments: commentIds,
            _comments_nextCursor: new_cursor,
            _comments_fetchStatus: FETCH_STATUS.SUCCESS
        }, );
        return newTable;
    },
    [ACTION_TYPES.GET_POST_EMOJIS + ACTION_TYPES._SENT]: (state, action) => {
        const {postcode} = action;
        const newTable = updateTable(state);
        newTable[postcode] = updatePost(newTable[postcode], {_emoji_fetchStatus: FETCH_STATUS.FETCHING});
        return newTable;
    },

    [ACTION_TYPES.GET_POST_EMOJIS + ACTION_TYPES._RECEIVED]: (state, action) => {
        const {emojis, postcode} = action;
        const newTable = updateTable(state);
        newTable[postcode] = updatePost(newTable[postcode], {
            emojis: emojis,
            _emoji_fetchStatus: FETCH_STATUS.SUCCESS
        }, );
        return newTable;
    }
});

const sliceReducer = combineReducers({
    appState: createReducer(APP_STATE.INITIALIZING, {}),
    appInit: appInitReducer,
    webSocketConnected: webSocketStateReducer,
    webSocketBridge: webSocketBridgeReducer,
    user: userReducer,
    userStatus: userStatusReducer,
    posts: postsReducer,
    postsStatus: postsStatusReducer,
    userSearchResults: userSearchResultsReducer,
    userSearchStatus: userSearchStatusReducer,
    trackedUsers: trackedUsersReducer,
    trackedUsersStatus: trackedUsersStatusReducer,
    aggregatedTrackingData: aggregatedTrackingDataReducer,
    unfollowingUsers: unfollowingUsersReducer,
    unfollowingUsersStatus: unfollowingUsersStatusReducer,
    comments: commentsReducer,
    commentsStatus: commentsStatusReducer,
    commentTable: commentTableReducer,
    postTable: postTableReducer
});

/**GLOBAL REDUCERS**/

const appStateGlobalReducer = (state = APP_STATE.INITIALIZING, action, globalState, oldGlobalState) => {
    if (globalState.appInit.length === 0 && state !== APP_STATE.ERROR)  {
        return APP_STATE.INITIALIZED;
    } else {
        return state;
    }
};

const globalReducer = (state = {}, action, oldState = {}) => {
    return combineReducers({
        appState: wrapGlobalReducer(appStateGlobalReducer, state, oldState),
        appInit: emptyReducer,
        webSocketConnected: emptyReducer,
        webSocketBridge: emptyReducer,
        user: emptyReducer,
        userStatus: emptyReducer,
        posts: emptyReducer,
        postsStatus: emptyReducer,
        userSearchResults: emptyReducer,
        userSearchStatus: emptyReducer,
        trackedUsers: emptyReducer,
        trackedUsersStatus: emptyReducer,
        aggregatedTrackingData: emptyReducer,
        unfollowingUsers: emptyReducer,
        unfollowingUsersStatus: emptyReducer,
        comments: emptyReducer,
        commentsStatus: emptyReducer,
        commentTable: emptyReducer,
        postTable: emptyReducer
    })(state, action);
};

export default function rootReducer(state = {}, action) {
    const intermediateState = sliceReducer(state, action);
    return globalReducer(intermediateState, action, state);
}
