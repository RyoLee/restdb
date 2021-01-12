-- kvdb.`data` definition

CREATE TABLE `data` (
  `k` varchar(64) NOT NULL,
  `v` text DEFAULT NULL,
  `p` varchar(64) NOT NULL,
  PRIMARY KEY (`k`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;