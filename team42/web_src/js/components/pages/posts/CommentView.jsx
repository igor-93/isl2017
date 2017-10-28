/**
 * Created by amirreza on 29.03.17.
 */
import React from 'react';
import ListItemView from "../../layout/ListItemView";
import moment from "moment";

import 'Styles/comments.scss';
import InstaUserLink from "../../layout/InstaUserLink";
import InstaText from "../../layout/InstaText";

export default class CommentView extends React.Component {

    render() {
        return (
            <ListItemView className={this.props.comment.sentiment}>
                <div className="comment-item-simple">
                    <div className="comment-head">
                        <div className="comment-head-left">
                            <span className="comment-user"><InstaUserLink username={this.props.comment.username}/></span>
                        </div>
                        <div className="comment-head-right">
                            <span className="comment-published-date">{moment(this.props.comment.date * 1000).fromNow()}</span>
                        </div>
                    </div>
                    <div className="comment-text" >
                        <InstaText text={this.props.comment.text}/>
                    </div>
                </div>
            </ListItemView>
        )
    }
}


CommentView.propTypes = {
    comment: React.PropTypes.object
};

CommentView.defaultProps = {};

CommentView.displayName = 'CommentView';