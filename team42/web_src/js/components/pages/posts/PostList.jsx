/**
 * Created by amirreza on 29.03.17.
 */

import React from 'react';
import ListView from "../../layout/ListView";
import PostListItem from './PostListItem'
import ContentBox from "../../layout/ContentBox";

export default class PostsList extends React.Component {

    render() {
        return (
            <ContentBox>
            <ListView emptyListText={'No posts found.'} onShowMoreClick={this.props.onShowMoreClick} loading={this.props.loading}>
                {this.props.posts.map((post, i) =>
                    <PostListItem
                        className="post-list-item"
                        key={i}
                        post={post}
                        onClick={() => this.props.onClick(post.code)}>
                    </PostListItem>
                )}
            </ListView>
            </ContentBox>
        )
    }
}


PostsList.propTypes = {
    posts: React.PropTypes.arrayOf(React.PropTypes.object),
    onClick: React.PropTypes.func,
    onShowMoreClick: React.PropTypes.func,
    loading: React.PropTypes.bool
};

PostsList.defaultProps = {
    posts: [],
    onClick: () => {},
    loading: false
};

PostsList.displayName = 'PostsList';
