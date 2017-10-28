/**
 * Created by raphi on 18.03.2017.
 */
import React from 'react';

import { connect } from 'react-redux';

import {APP_STATE} from '../constants';

import {SmartPostsPage} from './pages/posts/PostsPage';
import {SmartTargetsPage} from './pages/targets/TargetsPage';
import {SmartFollowingsPage} from './pages/followings/FollowingsPage';
import {SmartCommentsPage} from "./pages/comments/CommentsPage";
import {SmartUserPage} from "./pages/user/UserPage";
import ErrorPage from './pages/ErrorPage';

import LoadingSpinner from './LoadingSpinner';

import Header from './layout/Header';
import Main from './layout/Main';
import Footer from './layout/Footer';

import IconDef from './icons/IconDef';


import {fetchUserPosts} from '../store/actions';

import {trackedUsers, aggregatedTarget, unfollowUsers} from '../mockData';
import Icon from "./icons/Icon";
import HeartInHeartIcon from "./icons/HeartInHeartIcon";

import { Tabs, TabLink, TabContent } from 'react-tabs-redux';
import 'Styles/tabs.scss';
import IconText from "./icons/IconText";

export default class App extends React.Component {

    _renderUser() {
        return <SmartUserPage />;
    }

    _renderPosts() {
        return <SmartPostsPage />;
    }

    _renderTargets() {
        return <SmartTargetsPage />;
    }

    _renderFollowings() {
        return <SmartFollowingsPage />;
    }

    _renderComments() {
        return <SmartCommentsPage />;
    }

    render() {
        switch (this.props.appState) {
            case APP_STATE.INITIALIZING:
                return (
                    <div id="appContainer">
                        <LoadingSpinner absoluteCover/>
                        <div>Initializing Application...</div>
                    </div>
                );
                break;
            case APP_STATE.INITIALIZED:
                return (
                    <div id="appContainer">
                        <IconDef/>
                        <Header />
                        <Main>
                            {this._renderUser()}
                            <div className="row">
                                <div className="small-12 columns">
                                    <Tabs>
                                        <div className="tab-links">
                                            <TabLink to="tab1">
                                                <IconText iconName={'photo'} text={'Recent Posts'}/>
                                            </TabLink>
                                            <TabLink to="tab2">
                                                <IconText iconName={'comment'} text={'Recent Comments'}/>
                                            </TabLink>
                                            <TabLink to="tab3">
                                                <IconText iconName={'star'} text={'Tag/Time Suggestions'}/>
                                            </TabLink>
                                            <TabLink to="tab4">
                                                <IconText iconName={'user-times'} text={'Unfollow Suggestions'}/>
                                            </TabLink>
                                        </div>
                                        <TabContent for={'tab1'}>
                                            {this._renderPosts()}
                                        </TabContent>
                                        <TabContent for={'tab2'}>
                                            {this._renderComments()}
                                        </TabContent>
                                        <TabContent for={'tab3'}>
                                            {this._renderTargets()}
                                        </TabContent>
                                        <TabContent for={'tab4'}>
                                            {this._renderFollowings()}
                                        </TabContent>
                                    </Tabs>
                                </div>
                            </div>
                        </Main>
                        <Footer />
                    </div>
                );
                break;
            case APP_STATE.ERROR:
            default:
                return (
                    <div id="appContainer">
                        <ErrorPage/>
                    </div>
                );
                break;
        }
    }
}

App.propTypes = {
    appState: React.PropTypes.string.isRequired
};

App.defaultProps = {
    appState: APP_STATE.INITIALIZING
};

App.displayName = 'App';


/*CONTAINER COMPONENT*/
const mapStateToProps = (state, ownProps) => {
    return {
        appState: state.appState
    }
};

const mapDispatchToProps = (dispatch, ownProps) => {
    return {
    };
};

export const SmartApp = connect(
    mapStateToProps,
    mapDispatchToProps
)(App);