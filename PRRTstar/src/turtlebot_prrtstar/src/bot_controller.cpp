#include "math.h"
#include "ros/ros.h"
#include "geometry_msgs/Twist.h"
#include "tf2_ros/transform_listener.h"
#include "geometry_msgs/TransformStamped.h"
#include "geometry_msgs/Point.h"
#include "geometry_msgs/Quaternion.h"
#include "tf2/LinearMath/Quaternion.h"
#include "tf2_geometry_msgs/tf2_geometry_msgs.h"


int main(int argc, char **argv)
{
	ros::init(argc, argv, "bot_controller");

	ros::NodeHandle n;

	ros::Publisher vel_pub = n.advertise<geometry_msgs::Twist>("cmd_vel", 1000);
	
	ros::Publisher error_pub = n.advertise<geometry_msgs::Point>("error", 1000);
	
	tf2_ros::Buffer tfBuffer;
	tf2_ros::TransformListener tfl(tfBuffer);
	
	ros::Duration one_sec(1.0), ten_sec(10.0);
	ros::Time NOW;
	
	geometry_msgs::TransformStamped transformStamped_goal, transformStamped_bot, transformStamped_goal_prev, transformStamped_bot_prev;
	geometry_msgs::Twist msg;
	geometry_msgs::Point error_msg;
	geometry_msgs::Quaternion q_xaxis, q_final;
	tf2::Quaternion q_bot, q_bot_inverse, q_res, q;
	
	q_xaxis.x = 1.0;
	q_xaxis.y = 0.0;
	q_xaxis.z = 0.0;
	q_xaxis.w = 0.0;
	
	msg.linear.x = 0.0;
	msg.angular.z = 0.0;
	vel_pub.publish(msg);
	error_msg.x = 0.0;
	error_msg.y = 0.0;
	error_msg.z = 0.0;		
		
	error_pub.publish(error_msg);
	ten_sec.sleep();
  
	ros::spinOnce();
	
	double x_goal, y_goal, x_bot, y_bot, dx, dy, bot_angle, goal_angle, time_check;
	
	double Kpl = 0.5, Kpa = 5.03, Kdl = 0.01, Kda = 1.095; // Controller gains
	
	double dist, theta, vel, omega, now; // error terms and time
	
	double dist_prev = 0.0,  theta_prev = 0.0, then = 0.0; // error terms and time of previous state
	
	int count = 0;
	
	ros::Rate rate(1000);
	
	while(n.ok())
	{
		try
		{
			NOW = ros::Time::now();
			now = NOW.toSec();    
    	if (tfBuffer.canTransform("odom","goal",NOW,ros::Duration(0.1)))
    	{
      	  transformStamped_goal = tfBuffer.lookupTransform("odom","goal",NOW);
        	ROS_INFO("canTransformgggggggggg: TRUE");
    	}
    	else
    	{
        	ROS_INFO("canTransformgggggggggg: FALSE");
        	msg.linear.x = 0.0;
			msg.angular.z = 0.0;
			vel_pub.publish(msg);
			ros::spinOnce();
        	continue;
    	}
    	if (tfBuffer.canTransform("odom","base_footprint",NOW,ros::Duration(0.1)))
    	{
        	transformStamped_bot = tfBuffer.lookupTransform("odom","base_footprint",NOW);
        	ROS_INFO("canTransform: TRUE");
    	}
    	else
    	{
        	ROS_INFO("canTransform: FALSE");
    	}
		}
		catch(tf2::TransformException &ex)
		{
			ROS_WARN("%s",ex.what());
			one_sec.sleep();
			continue;
		}
				
		x_goal = transformStamped_goal.transform.translation.x;
		y_goal = transformStamped_goal.transform.translation.y;
		x_bot = transformStamped_bot.transform.translation.x;
		y_bot = transformStamped_bot.transform.translation.y;
		
		tf2::fromMsg(transformStamped_bot.transform.rotation, q_bot);
		transformStamped_bot.transform.rotation.x = -transformStamped_bot.transform.rotation.x;
		transformStamped_bot.transform.rotation.y = -transformStamped_bot.transform.rotation.y;
		transformStamped_bot.transform.rotation.z = -transformStamped_bot.transform.rotation.z;
		tf2::fromMsg(transformStamped_bot.transform.rotation, q_bot_inverse);
		tf2::fromMsg(q_xaxis, q);
		
		q_res = q_bot*q*q_bot_inverse;
		q_res.normalize();
		q_final = tf2::toMsg(q_res);
		
		dx = x_goal-x_bot;
		dy = y_goal-y_bot;
		dist = sqrt(dx*dx+dy*dy);
		vel = (dist-dist_prev)/(now-then);
		bot_angle = atan2(q_final.y,q_final.x);
		goal_angle = atan2(dy,dx);
		
		if (bot_angle < 0.0)
		{
			bot_angle = 2.0*M_PIq+bot_angle;
		}
		if (goal_angle < 0.0)
		{
			goal_angle = 2.0*M_PIq+goal_angle;
		}
		
		theta = goal_angle-bot_angle;
		
		if (fabs(theta) > M_PIq)
		{
			if (theta > 0)
			{
				theta = theta-2.0*M_PIq;
			}
			else
			{
				theta = theta+2.0*M_PIq;
			}
		}
		
		if (dx == 0.0 && dy == 0.0)
		{
			theta = 0.0;
		}

		omega = (theta-theta_prev)/(now-then);
		
		if (count == 0)
		{
			vel = 0.0;
			omega = 0.0;
		}
			
		msg.linear.x = Kpl*dist + Kdl*vel;
		msg.angular.z = Kpa*theta + Kda*omega;
		
		if (dist < 0.0001)
		{
			msg.angular.z = 0.0;
		}
		if (dist < 0.0001)
		{
			msg.linear.x = 0.0;
		}
				
		//ROS_INFO("vel - %f, omega - %f, dist = %f, theta = %f\n", vel, omega, dist, theta);
		
			
		error_msg.x = theta;
		error_msg.y = omega;
		error_msg.z = bot_angle;		
		
		error_pub.publish(error_msg);
		
		dist_prev = dist;
		theta_prev = theta;
		then = now;

		//ROS_INFO("goal - {%f, %f} goal_angle - %f, bot_angle - %f, theta - %f\n", dx, dy, goal_angle, bot_angle, theta);
		vel_pub.publish(msg);
	  
		ros::spinOnce();
		count = 1;
		rate.sleep();
	}

	return 0;
}
