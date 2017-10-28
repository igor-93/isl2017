import React from 'react';
import posts from './posts';
import PageView from "../../layout/PageView";
import {SmartPostListItemDetail} from "./PostListItemDetail";
import PostList from './PostList';

import {FETCH_STATUS} from '../../../constants';

import { connect } from 'react-redux';

import {fetchUserPosts} from '../../../store/actions';
import Row from "../../layout/Row";
import Columns from "../../layout/Columns";

export default class PostsPage extends React.Component {
    constructor(props) {
        super();
        this.state = {
            current_postcode: null,
        };
    }

    componentDidMount() {
        this.props.fetchPosts();
    }

    handleClick(code) {
        this.setState({
            current_postcode: code,
        });
    }

    _hideDetails() {
        this.setState({current_postcode: null});
    }

    _showMore() {
        this.props.fetchMorePosts();
    }

    render() {
        const postsList = Object.values(this.props.postTable);
        let curPost = this.props.postTable[this.state.current_postcode];
        if (curPost) {
            // create copy
            curPost = Object.assign({}, curPost);
            // dereference comments
            curPost.comments = curPost.comments.map((key) => {
                const comm = this.props.commentTable[key];
                if (comm === undefined) {
                    const self = this;
                    console.log('undefined comment', curPost);
                }
                return comm;
            });
        }
        let showMore = (e) => this._showMore(e);
        if (this.props.postsStatus.nextCursor === null) {
            showMore = undefined;
        }
        const isLoading = this.props.postsStatus.fetchStatus === FETCH_STATUS.FETCHING;

        const isExtended = Boolean(this.state.current_postcode);
        const postsOrdered = postsList.sort((p0, p1) => p1.date - p0.date);
        return (
            <PageView extended={isExtended} onHideDetails={() => this._hideDetails()}>
                <Row>
                    <Columns cols={[12, 6, 4]} className={'page-list-wrapper'}>
                        <PostList loading={isLoading} id="post-list" posts={postsOrdered} onClick={i => this.handleClick(i)} onShowMoreClick={showMore}/>
                    </Columns>

                    <Columns cols={[12, 12, 8]} className="page-details-wrapper">
                        <SmartPostListItemDetail post={curPost}/>
                    </Columns>
                </Row>
            </PageView>
        )
    }
}


PostsPage.propTypes = {
    fetchPosts: React.PropTypes.func,
    fetchMorePosts: React.PropTypes.func,
    postTable: React.PropTypes.object,
    postsStatus: React.PropTypes.object,
    commentTable: React.PropTypes.object
};

PostsPage.defaultProps = {
    postsStatus: {fetchStatus: null, nextCursor: 1}
};

PostsPage.displayName = 'PostsPage';

/*CONTAINER COMPONENT*/
const mapStateToProps = (state, ownProps) => {
    return {
        postsStatus: state.postsStatus,
        postTable: state.postTable,
        commentTable: state.commentTable
    }
};

const mapDispatchToProps = (dispatch, ownProps) => {
    return {
        fetchPosts: () => dispatch(fetchUserPosts()),
        fetchMorePosts: () => dispatch(fetchUserPosts(true))
    };
};

export const SmartPostsPage = connect(
    mapStateToProps,
    mapDispatchToProps
)(PostsPage);