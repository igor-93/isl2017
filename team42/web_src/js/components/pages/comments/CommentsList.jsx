import React from 'react';
import ListView from "../../layout/ListView";
import CommentsListItem from "./CommentsListItem";
import SortFilterBar from "../../layout/SortFilterBar";

import {SENTIMENT} from '../../../constants';
import FAIcon from "../../icons/FAIcon";
import ContentBox from "../../layout/ContentBox";

export default class CommentsList extends React.Component {

    constructor(props) {
        super(props);
        this.state = {filterFunc: (items) => items};
    }

    _onVisibleItemsChanged(filterFunc) {
        this.setState({filterFunc: filterFunc});
    }

    render() {
        const visibleComments = this.state.filterFunc(this.props.comments);

        const itemsRendered = visibleComments.map((comment, i) => {
                    const commentWithPost = Object.assign({}, comment, {post: this.props.postTable[comment.post_code]});
                    return (
                        <CommentsListItem
                            className="comments-list-item"
                            key={i}
                            comment={commentWithPost}
                            onClick={() => this.props.onClick(comment.id)} />
                    );});

        return (
            <ContentBox>
            <ListView emptyListText={'No comments found for recent posts.'}
                loading={this.props.loading}
                      filters={CommentsList.filters}
                        onShowMoreClick={this.props.onShowMoreClick}
                      onItemFuncChanged={(items) => this._onVisibleItemsChanged(items)}>
                {itemsRendered}
            </ListView>
            </ContentBox>
        );
    }

}

CommentsList.propTypes = {
    comments: React.PropTypes.arrayOf(React.PropTypes.object),
    onClick: React.PropTypes.func,
    loading: React.PropTypes.bool,
    selectedId: React.PropTypes.string,
    postTable: React.PropTypes.object,
    onShowMoreClick: React.PropTypes.func
};

CommentsList.defaultProps = {
    comments: [],
    onClick: () => {},
    loading: false,
    selectedId: '',
    postTable: {}
};

CommentsList.displayName = 'CommentsList';

CommentsList.filters = [{
    name: 'negOnly',
    displayName: <FAIcon iconName={'thumbs-o-down'}/>,
    filterFunc: (comment) => (comment.sentiment === SENTIMENT.NEGATIVE || comment.sentiment === SENTIMENT.VERY_NEGATIVE)
}];