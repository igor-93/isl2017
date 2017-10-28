import React from 'react';
import ListItemDetailView from "../../layout/ListItemDetailView";
import StatsBox from "../../StatsBox";
import InstaText from "../../layout/InstaText";
import InstaUserLink from "../../layout/InstaUserLink";
import ContentBox from "../../layout/ContentBox";
import FAIcon from "../../icons/FAIcon";
import moment from "moment";
import UserCard from "../user/UserCard";

export default class FollowingsItemDetails extends React.Component {

    render() {
        if (!this.props.user) {
            return <ListItemDetailView/>
        }

        const actions = [{
                href: 'http://www.instagram.com/' + this.props.user.username,
                display: <FAIcon iconName={'user-times'}/>,
                className: 'icon-button',
                description: 'unfollow (redirect)'
        }];

        return (
                <ListItemDetailView>
                    <ContentBox actions={actions}>
                    <div className="item-details following-details">
                        <div className="item-details-content-box">
                            <UserCard
                                userName={this.props.user.username}
                                fullName={this.props.user.full_name}
                                imgSrc={this.props.user.img_src_url}
                            />
                            <div className="item-details-stats">
                                <div className="stats-box-list">
                                    <StatsBox title={'Posts'} value={this.props.user.n_posts}/>
                                    <StatsBox title={'Follows'} value={this.props.user.n_follows}/>
                                    <StatsBox title={'Followers'} value={this.props.user.n_followed_by}/>
                                </div>
                                <div className="stats-box-list">
                                    <StatsBox title={'Activity Rating'} value={this.props.user.activity}/>
                                    <StatsBox title={'Last Post'} value={moment(1000 * this.props.user.last_post_ts).fromNow()}/>
                                </div>
                            </div>
                        </div>
                    </div>
                    </ContentBox>
                </ListItemDetailView>
        );
    }

}

FollowingsItemDetails.propTypes = {
    user: React.PropTypes.object
};

FollowingsItemDetails.defaultProps = {
    user: {}
};

FollowingsItemDetails.displayName = 'FollowingsItemDetails';