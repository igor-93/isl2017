import React from 'react';
import ContentBox from "../../layout/ContentBox";
import UserCard from "./UserCard";
import LoadingSpinner from "../../LoadingSpinner";
import {FETCH_STATUS} from '../../../constants';
import moment from 'moment';

import { connect } from 'react-redux';
import StatsBox from "../../StatsBox";
import TimeSlotChart from "../targets/TimeSlotChart";

import {fetchAggregatedTrackingData, fetchUserProfile} from '../../../store/actions';
import WordCloudComponent from "../../layout/WordCloudComponent";


export default class UserPage extends React.Component {

    constructor(props) {
        super(props);
    }

    componentDidMount() {
        this.props.fetchAggregatedData();
        this.props.fetchUserData();
    }

    _onWordCloudClick(item, dim, event) {
        const el = document.getElementById('userPageTagInput');
        el.textContent = '#' + item[0];
    }

    _renderUser() {
        if (this.props.user && !this.props.userLoading) {
            const {username, full_name, img_src_url} = this.props.user;
            const now = Date.now();
            let lastPostClass = '';
            let lastPostText = '-';
            const lastPostTs = this.props.user.last_post_ts * 1000;
            if (lastPostTs) {
                lastPostText = moment(lastPostTs).fromNow();
                const weeks = (now - lastPostTs) / UserPage.WEEK_MS;
                if (weeks > 2) {
                    lastPostClass += 'alert';
                } else if (weeks > 1) {
                    lastPostClass += 'warning';
                }
            }
            return (
                <div className="user-details">
                    <UserCard userName={username} fullName={full_name} imgSrc={img_src_url}/>
                    <div className="user-stats">
                        <StatsBox title={'Posts'} value={this.props.user.n_posts}/>
                        <StatsBox title={'Follows'} value={this.props.user.n_follows}/>
                        <StatsBox title={'Followers'} value={this.props.user.n_followed_by}/>
                        <StatsBox title={'Last Post'} value={lastPostText} className={lastPostClass}/>
                    </div>
                </div>
            );
        } else {
            return <LoadingSpinner fullHeight/>
        }
    }

    _renderTime() {
        if (this.props.aggregatedData && !this.props.aggregatedDataLoading) {
            return <TimeSlotChart timeSlots={this.props.aggregatedData.best_time}/>;
        } else {
            return <LoadingSpinner fullHeight/>
        }

    }

    _renderTags() {
        if (this.props.aggregatedData && !this.props.aggregatedDataLoading) {
            return (
                <div>
                    <WordCloudComponent onItemClick={(item, dim, event) => this._onWordCloudClick(item, dim, event)} list={this.props.aggregatedData.best_tags} emptyListMsg={'No tags found.'} canvasId="userWordCloudCanvas"/>
                    <div className="word-cloud-single-tag-display" id="userPageTagInput" > </div>
                </div>
            );
        } else {
            return <LoadingSpinner fullHeight/>
        }
    }

    render() {
        return (
            <div>
            <div className="row">
                <div className="columns small-12">
                    <ContentBox title={'Me'}>
                        {this._renderUser()}
                    </ContentBox>
                </div>

            </div>
                <div className="row">
                    <div className="columns small-12 medium-6">
                    <ContentBox title={'Best Time to Post'}>
                        {this._renderTime()}
                    </ContentBox>
                </div>
                <div className="columns small-12 medium-6">
                    <ContentBox title={'Best Tags'}>
                        {this._renderTags()}
                    </ContentBox>
                </div>
                </div>
            </div>
        );
    }

}

UserPage.propTypes = {
    user: React.PropTypes.object,
    aggregatedData: React.PropTypes.object,
    userLoading: React.PropTypes.bool,
    aggregatedDataLoading: React.PropTypes.bool,
    fetchAggregatedData: React.PropTypes.func,
    fetchUserData: React.PropTypes.func
};

UserPage.defaultProps = {};

UserPage.displayName = 'UserPage';

UserPage.WEEK_MS = 604800000;

/*CONTAINER COMPONENT*/
const mapStateToProps = (state, ownProps) => {
    return {
        userLoading: state.userStatus.fetchStatus === FETCH_STATUS.FETCHING,
        user: state.user,
        aggregatedData: state.aggregatedTrackingData,
        aggregatedDataLoading: !state.aggregatedTrackingData._ts
    }
};

const mapDispatchToProps = (dispatch, ownProps) => {
    return {
        fetchAggregatedData: () => dispatch(fetchAggregatedTrackingData()),
        fetchUserData: ()=> dispatch(fetchUserProfile())
    };
};

export const SmartUserPage = connect(
    mapStateToProps,
    mapDispatchToProps
)(UserPage);
