import React from 'react';

import PageView from '../../layout/PageView';
import CommentsList from "./CommentsList";
import CommentsItemDetails from "./CommentsItemDetails";

import { connect } from 'react-redux';

import {FETCH_STATUS} from '../../../constants';

import {fetchRecentComments} from '../../../store/actions';

import 'Styles/comments.scss';
import Row from "../../layout/Row";
import Columns from "../../layout/Columns";

export default class CommentsPage extends React.Component {

    constructor(props) {
        super();
        this.state = {
            selected_comment_id: null,
        };
    }

    componentDidMount() {
        this.props.fetchComments();
    }

    handleClick(i) {
        this.setState({
            selected_comment_id: i,
        });
    }

    _hideDetails() {
        this.setState({selected_comment_id: null});
    }

    render() {
        const commentsList = Object.values(this.props.commentTable);
        const isExtended = Boolean(this.state.selected_comment_id);
        const commentsLoading = this.props.commentsStatus.fetchStatus === FETCH_STATUS.FETCHING;
        const selectedComment = this.props.commentTable[this.state.selected_comment_id];
        if (selectedComment) {
            selectedComment.post = this.props.postTable[selectedComment.post_code];
        }

        const commentsOrdered = commentsList.filter((c) => c.date >= this.props.commentsStatus.oldest_ts).sort((c0, c1) => c1.date - c0.date);

        const showMoreClick = this.props.commentsStatus.oldest_ts === -1 ? null : () => this.props.fetchComments();

        return (
            <PageView extended={isExtended} onHideDetails={() => this._hideDetails()}>
                <Row>
                    <Columns cols={[12, 6, 4]} className={'page-list-wrapper'}>
                        <CommentsList loading={commentsLoading} id="comments-list"
                                      comments={commentsOrdered}
                                      postTable={this.props.postTable}
                                      onClick={i => this.handleClick(i)}
                                      onShowMoreClick={showMoreClick}
                        />
                    </Columns>
                    <Columns cols={[12, 12, 8]} className="page-details-wrapper">
                        <CommentsItemDetails comment={selectedComment} />
                    </Columns>
                </Row>

            </PageView>
        );
    }

}

CommentsPage.propTypes = {
    commentTable: React.PropTypes.object,
    postTable: React.PropTypes.object,
    commentsStatus: React.PropTypes.object,
    fetchComments: React.PropTypes.func

};

CommentsPage.defaultProps = {
    commentTable: {},
    postTable: {}
};

CommentsPage.displayName = 'CommentsPage';

/*CONTAINER COMPONENT*/
const mapStateToProps = (state, ownProps) => {
    return {
        commentTable: state.commentTable,
        postTable: state.postTable,
        commentsStatus: state.commentsStatus
    }
};

const mapDispatchToProps = (dispatch, ownProps) => {
    return {
        fetchComments: () => dispatch(fetchRecentComments())
    };
};

export const SmartCommentsPage = connect(
    mapStateToProps,
    mapDispatchToProps
)(CommentsPage);

    
