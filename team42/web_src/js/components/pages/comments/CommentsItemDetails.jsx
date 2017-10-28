import React from 'react';
import ListItemDetailView from "../../layout/ListItemDetailView";
import StatsBox from "../../StatsBox";

import moment from 'moment';
import TextBox from "../../TextBox";
import InstaUserLink from "../../layout/InstaUserLink";
import InstaText from "../../layout/InstaText";
import UserCard from "../user/UserCard";
import ContentBox from "../../layout/ContentBox";
import FAIcon from "../../icons/FAIcon";

export default class CommentsItemDetails extends React.Component {

    render() {
        if (!this.props.comment) {
            return <ListItemDetailView/>
        }

        const post = this.props.comment.post || {};
        const postTS = post.date * 1000;

        const commentActions = [{
            href: 'http://www.instagram.com/p/' + post.code,
            display: <FAIcon iconName={'reply'}/>,
            className: 'icon-button',
            description: 'reply (redirect)'
        }];

        const postActions = [{
            href: 'http://www.instagram.com/p/' + post.code,
            display: <FAIcon iconName={'instagram'}/>,
            className: 'icon-button',
            description: 'show on Instagram'
        }];

        return (
            <ListItemDetailView>
                <div className="item-details comment-details">
                    <ContentBox title={'Comment'} actions={commentActions} headerRight={<span>{moment(this.props.comment.date * 1000).fromNow()}</span>}>
                        <div className="item-details-content-box">
                            <UserCard imgSrc={this.props.comment.user_img_src_url} userName={this.props.comment.username}/>
                            <div className="item-details-stats">
                                <div className={'comment-details-text ' + this.props.comment.sentiment}>
                                    <InstaText text={this.props.comment.text}/>
                                </div>
                            </div>
                        </div>
                    </ContentBox>
                    <ContentBox title={'Post'} actions={postActions} headerRight={<span>{moment(postTS).fromNow()}</span>}>
                        <div className="item-details-content-box">
                            <div className="item-img" >
                                <img src={post.img_src_url}/>
                            </div>
                            <div className="item-details-stats">
                                <InstaText text={post.caption} />
                            </div>
                        </div>
                    </ContentBox>
                </div>
            </ListItemDetailView>
        );
    }

}

CommentsItemDetails.propTypes = {
    comment: React.PropTypes.object
};

CommentsItemDetails.defaultProps = {
    comment: {}
};

CommentsItemDetails.displayName = 'CommentsItemDetails';