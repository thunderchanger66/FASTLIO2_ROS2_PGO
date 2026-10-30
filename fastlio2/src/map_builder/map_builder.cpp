#include "map_builder.h"
MapBuilder::MapBuilder(Config &config, std::shared_ptr<IESKF> kf) : m_config(config), m_kf(kf)
{
    m_imu_processor = std::make_shared<IMUProcessor>(config, kf);
    m_lidar_processor = std::make_shared<LidarProcessor>(config, kf);
    m_status = BuilderStatus::IMU_INIT;
}

bool MapBuilder::process(SyncPackage &package)
{
    if (m_status == BuilderStatus::IMU_INIT)
    {
        if (m_imu_processor->initialize(package))
            m_status = BuilderStatus::MAP_INIT;
        return false;
    }

    const State state_before_scan = m_kf->x();
    const M21D covariance_before_scan = m_kf->P();
    m_imu_processor->undistort(package);
    if (!m_imu_processor->last_undistort_valid())
    {
        m_kf->x() = state_before_scan;
        m_kf->P() = covariance_before_scan;
        return false;
    }

    if (m_status == BuilderStatus::MAP_INIT)
    {
        CloudType::Ptr cloud_world = LidarProcessor::transformCloud(package.cloud, m_lidar_processor->r_wl(), m_lidar_processor->t_wl());
        m_lidar_processor->initCloudMap(cloud_world->points);
        m_status = BuilderStatus::MAPPING;
        return false;
    }
    
    // Keep the valid IMU prediction when LiDAR has no constraints. Rolling
    // back across time here would desynchronize the filter from IMUProcessor.
    return m_lidar_processor->process(package);
}
