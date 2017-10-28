import React from 'react';
import ListItemDetailView from "../../layout/ListItemDetailView";
import TimeSlotChart from "./TimeSlotChart";
import LoadingSpinner from "../../LoadingSpinner";
import StatsBox from "../../StatsBox";
import WordCloud from "wordcloud"
import InstaUserLink from "../../layout/InstaUserLink";
import ContentBox from "../../layout/ContentBox";
import FAIcon from "../../icons/FAIcon";
import UserCard from "../user/UserCard";
import WordCloudComponent from "../../layout/WordCloudComponent";

export default class TargetsItemDetails extends React.Component {

    _renderBestTags() {
        return (<div>
            <WordCloudComponent canvasId="wordCloudCanvas" list={this.props.user.best_tags} onItemClick={(item, dim, event) => this._onWordCloudClick(item, dim, event)}/>
            <div className="word-cloud-single-tag-display" id="targetDetailsTagInput" > </div>
        </div>);
    }

    _onWordCloudClick(item, dim, event) {
        const el = document.getElementById('targetDetailsTagInput');
        el.textContent = '#' + item[0];
    }

    _renderBestTime() {
        return <TimeSlotChart timeSlots={this.props.user.best_time}/>;
    }

    render() {
        if (!this.props.user) {
            return <ListItemDetailView/>
        }

        if (!this.props.user._details_ts) {
            return (
                <ListItemDetailView>
                    <LoadingSpinner fullHeight/>
                </ListItemDetailView>
            );
        }

        const actions = [{
                onClick: () => this.props.onRemoveUser(this.props.user),
                display: <FAIcon iconName={'trash'}/>,
                className: 'icon-button',
                description: 'remove user'
        }];

        return (
            <ListItemDetailView>
                    <div className="item-details target-details">
                        <ContentBox actions={actions}>
                        <div className="item-details-content-box">
                            <UserCard
                                userName={this.props.user.username}
                                fullName={this.props.user.full_name}
                                imgSrc={this.props.user.img_src_url}/>
                            <div className="item-details-stats">
                                <div className="stats-box-list">
                                    <StatsBox title={'Posts'} value={this.props.user.n_posts}/>
                                    <StatsBox title={'Follows'} value={this.props.user.n_follows}/>
                                    <StatsBox title={'Followers'} value={this.props.user.n_followed_by}/>
                                </div>
                            </div>
                        </div>
                        {this._renderBestTags()}
                        {this._renderBestTime()}
                        </ContentBox>
                    </div>
                </ListItemDetailView>
        );
    }

}

TargetsItemDetails.propTypes = {
    user: React.PropTypes.object,
    onRemoveUser: React.PropTypes.func
};

TargetsItemDetails.defaultProps = {
    user: {},
    onRemoveUser: () => {}
};

TargetsItemDetails.displayName = 'TargetsItemDetails';