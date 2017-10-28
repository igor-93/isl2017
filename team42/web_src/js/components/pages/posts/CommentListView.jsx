/**
 * Created by amirreza on 29.03.17.
 */

import React from 'react';

import ListView from "../../layout/ListView";
import CommentView from './CommentView'
export default class CommentList extends React.Component {

    render() {
        const commentsOrdered = this.props.comments.sort((p0, p1) => p1.date - p0.date);
        return (
            <ListView emptyListText={'No comments found.'} onShowMoreClick={this.props.onShowMoreClick} loading={this.props.loading}>
                {commentsOrdered.map((comment, i) =>
                    <CommentView id="comment-view"
                        key={i}
                        comment={comment}>
                    </CommentView>
                )}
            </ListView>
        )
    }
}


CommentList.propTypes = {
    comments: React.PropTypes.array,
    onShowMoreClick: React.PropTypes.func,
    loading: React.PropTypes.bool
};

CommentList.defaultProps = {
    loading: false,
    comments: []
};

CommentList.displayName = 'CommentList';