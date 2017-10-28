import React from 'react';
import ListItemView from "../../layout/ListItemView";
import moment from "moment";
import InstaUserLink from "../../layout/InstaUserLink";
import InstaText from "../../layout/InstaText";


export default class CommentsListItem extends React.Component {

    render() {
        const post = this.props.comment.post || {};
        return (
            <ListItemView onClick={() => this.props.onClick()} selected={this.props.selected} className={this.props.comment.sentiment}>
                <div className="comment-list-item list-item-content">
                    <div className="item-img">
                        <img src={post.img_src_url}/>
                    </div>
                    <div className="list-item-info">
                        <div className="comment-head">
                            <div className="comment-head-left">
                                <span className="comment-user"><InstaUserLink username={this.props.comment.username}/></span>
                            </div>
                            <div className="comment-head-right">
                                <span className="comment-published-date">{moment(this.props.comment.date * 1000).fromNow()}</span>
                            </div>
                        </div>
                        <div className={"comment-text " + this.props.comment.sentiment}>
                            <InstaText text={this.props.comment.text} />
                        </div>
                    </div>
                </div>
            </ListItemView>
        );
    }

}

CommentsListItem.propTypes = {
    onClick: React.PropTypes.func,
    comment: React.PropTypes.object,
    selected: React.PropTypes.bool
};

CommentsListItem.defaultProps = {
    onClick: () => {},
    comment: {},
    selected: false
};

CommentsListItem.displayName = 'CommentsListItem';