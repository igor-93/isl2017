/**
 * Created by amirreza on 29.03.17.
 */

import React from 'react';
import ListItemDetailView from "../../layout/ListItemDetailView";
import CommentList from './CommentListView'
import moment from 'moment';
import StatsBox from "../../StatsBox";
import TextBox from "../../TextBox";

import {FETCH_STATUS} from '../../../constants';

import { connect } from 'react-redux';

import {fetchPostComments, fetchPostEmojis} from '../../../store/actions';
import TargetsPage from "../targets/TargetsPage";
import InstaText from "../../layout/InstaText";
import ContentBox from "../../layout/ContentBox";
import FAIcon from "../../icons/FAIcon";
import LoadingSpinner from "../../LoadingSpinner";

export default class PostListItemDetail extends React.Component {

    componentDidUpdate() {
        if (this.props.post && !this.props.post._comments_fetchStatus) {
            this._loadMoreComments();
        }
        if (this.props.post && !this.props.post._emoji_fetchStatus) {
            this.props.fetchEmojis(this.props.post);
        }
    }

    _loadMoreComments() {
        if (this.props.post) {
            this.props.fetchComments(this.props.post);
        }
    }

    _renderEmojis() {
        if (this.props.post.emojis) {
            const emojiRendered = [];
            this.props.post.emojis.forEach((emoji) => {
                emojiRendered.push((
                    <div className="reaction" key={emoji[0]}>
                        <span className="reaction-text">{emoji[0]}</span>
                        <span className="reaction-count">{emoji[1]}</span>
                    </div>
                ))
            });

            return (
                <div className="reactions-list">
                    {emojiRendered}
                </div>
            );
        } else {
            return <LoadingSpinner/>
        }
    }

    render() {
        if (!this.props.post) {
            return <ContentBox><ListItemDetailView /></ContentBox>;
        } else {
            const actions = [{
                href: 'http://www.instagram.com/p/' + this.props.post.code,
                display: <FAIcon iconName={'instagram'}/>,
                className: 'icon-button',
                description: 'show on Instagram'
            }];
            const isCommentsLoading = this.props.post._comments_fetchStatus === FETCH_STATUS.FETCHING;
            const showMore = this.props.post._comments_nextCursor ? () => this._loadMoreComments() : undefined;
            const postTS = this.props.post.date * 1000;
            return (
                <ListItemDetailView>
                    <div className="item-details post-details">
                        <ContentBox title={'Post'} actions={actions} headerRight={<span>{moment(postTS).fromNow()}</span>}>
                            <div className="item-details-content-box post-details-info">
                                <div className="item-img">
                                    <img src={this.props.post.img_src_url}/>
                                </div>
                                <div className="item-details-stats">
                                    <div className="stats-box-list">
                                        <StatsBox title={'Likes'} value={this.props.post.n_likes} />
                                        <StatsBox title={'Likes/min'} value={(60 * this.props.post.n_likes / (0.001 * (Date.now() - postTS))).toFixed(2)} />
                                        <StatsBox title={'Comments'} value={this.props.post.n_comments} />
                                    </div>
                                    <div className="stats-box">
                                        <div className="stats-box-title">REACTIONS</div>
                                        {this._renderEmojis()}
                                    </div>
                                    <div>
                                        <InstaText text={this.props.post.caption}/>
                                    </div>
                                </div>
                            </div>
                        </ContentBox>
                        <ContentBox title={'Comments'}>
                            <div   className={'post-comment-list'}>
                                <CommentList loading={isCommentsLoading} comments={this.props.post.comments} onShowMoreClick={showMore}/>
                            </div>
                        </ContentBox>
                    </div>
                </ListItemDetailView>
            )
        }
    }
}

PostListItemDetail.propTypes = {
    post: React.PropTypes.object,
    fetchComments: React.PropTypes.func,
    fetchEmojis: React.PropTypes.func
};

PostListItemDetail.defaultProps = {};

PostListItemDetail.displayName = 'PostListItemDetail';

/*CONTAINER COMPONENT*/
const mapStateToProps = (state, ownProps) => {
    return {
    }
};

const mapDispatchToProps = (dispatch, ownProps) => {
    return {
        fetchComments: (post) => dispatch(fetchPostComments(post, true)),
        fetchEmojis: (post) => dispatch(fetchPostEmojis(post.code))
    };
};

export const SmartPostListItemDetail = connect(
    mapStateToProps,
    mapDispatchToProps
)(PostListItemDetail);