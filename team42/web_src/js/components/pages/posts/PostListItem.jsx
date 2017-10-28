/**
 * Created by amirreza on 29.03.17.
 */

import React from 'react';
import ListItemView from "../../layout/ListItemView";
import moment from 'moment';
import HeartInHeartIcon from "../../icons/HeartInHeartIcon";
import FAIcon from "../../icons/FAIcon";

export default class PostsListItem extends React.Component {

    render() {
        const postTS = this.props.post.date * 1000;
        return (
            <ListItemView onClick={() => this.props.onClick()}>
                <div className="list-item-content post-list-item">
                    <div className="item-img">
                        <img src={this.props.post.img_src_url}/>
                    </div>
                    <div className="list-item-info">
                        <div className="post-list-item-header">{moment(postTS).fromNow()}</div>
                        <div className="post-list-item-content">
                            <div className="post-likes"><FAIcon iconName={'heart'}/> {this.props.post.n_likes}</div>
                            <div className="post-likes-pm"><FAIcon iconName={'heartbeat'}/> {((60* this.props.post.n_likes) / (0.001 * (Date.now() - postTS))).toFixed(2)} / min</div>
                            <div className="post-comments"><FAIcon iconName={'comment'}/> {this.props.post.n_comments}</div>
                        </div>
                    </div>
                </div>
            </ListItemView>
        )
    }
}




PostsListItem.propTypes = {
    post: React.PropTypes.object
};

PostsListItem.defaultProps = {
    post: {}
};

PostsListItem.displayName = 'PostsListItem';
