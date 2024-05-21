-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 03, 2024 at 08:19 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `airplane network`
--

-- --------------------------------------------------------

--
-- Table structure for table `airline`
--

CREATE TABLE `airline` (
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `airline`
--

INSERT INTO `airline` (`name`) VALUES
('United');

-- --------------------------------------------------------

--
-- Table structure for table `airline_staff`
--

CREATE TABLE `airline_staff` (
  `username` varchar(255) NOT NULL,
  `airline_name` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `date_of_birth` date NOT NULL,
  `primary_email` varchar(255) NOT NULL,
  `primary_phone` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `airline_staff`
--

INSERT INTO `airline_staff` (`username`, `airline_name`, `password`, `first_name`, `last_name`, `date_of_birth`, `primary_email`, `primary_phone`) VALUES
('admin', 'United', '$2b$12$GmXv62u.tvxn9qWvQdfHMeMZUZ6gFE.9e1t3wz0kfipwH/NLA4zMy', 'Roe', 'Jones', '1978-05-25', 'staff@nyu.edu', '11122223333');

-- --------------------------------------------------------

--
-- Table structure for table `airplane`
--

CREATE TABLE `airplane` (
  `airplane_id` varchar(255) NOT NULL,
  `airline_name` varchar(255) NOT NULL,
  `number_of_seats` int(11) NOT NULL,
  `manufacturer` varchar(255) NOT NULL,
  `model_number` varchar(255) NOT NULL,
  `manufacturing_date` date NOT NULL,
  `age` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `airplane`
--

INSERT INTO `airplane` (`airplane_id`, `airline_name`, `number_of_seats`, `manufacturer`, `model_number`, `manufacturing_date`, `age`) VALUES
('1', 'United', 4, 'Boeing', 'B-101', '2013-05-02', 11),
('2', 'United', 4, 'Airbus', 'A-101', '2011-05-02', 13),
('3', 'United', 50, 'Boeing', 'B-101', '2015-05-02', 9);

-- --------------------------------------------------------

--
-- Table structure for table `airport`
--

CREATE TABLE `airport` (
  `code` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `country` varchar(255) NOT NULL,
  `number_of_terminals` int(11) NOT NULL,
  `type` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `airport`
--

INSERT INTO `airport` (`code`, `name`, `city`, `country`, `number_of_terminals`, `type`) VALUES
('BEI', 'BEI', 'Beijing', 'China', 2, 'Both'),
('BOS', 'BOS', 'Boston', 'USA', 2, 'Both'),
('HKA', 'HKA', 'Hong Kong', 'China', 2, 'Both'),
('JFK', 'JFK', 'NYC', 'USA', 4, 'Both'),
('LAX', 'LAX', 'Los Angeles', 'USA', 2, 'Both'),
('PVG', 'PVG', 'Shanghai', 'China', 2, 'Both'),
('SFO', 'SFO', 'San Francisco', 'USA', 2, 'Both'),
('SHEN', 'SHEN', 'Shenzhen', 'China', 2, 'Both');

-- --------------------------------------------------------

--
-- Table structure for table `buys`
--

CREATE TABLE `buys` (
  `ticket_id` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `card_type` varchar(255) NOT NULL,
  `card_number` char(255) DEFAULT NULL,
  `name_on_card` varchar(255) NOT NULL,
  `expiration_date` date NOT NULL,
  `purchase_date` date NOT NULL,
  `purchase_time` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `buys`
--

INSERT INTO `buys` (`ticket_id`, `email`, `card_type`, `card_number`, `name_on_card`, `expiration_date`, `purchase_date`, `purchase_time`) VALUES
('1', 'testcustomer@nyu.edu', 'credit', '1111-2222-3333-4444', ' Jon Snow', '2025-03-30', '2024-01-07', '11:55:55'),
('2', 'user1@nyu.edu', 'credit', '1111-2222-3333-5555', 'Alice Bob', '2025-03-30', '2024-01-06', '11:55:55'),
('3', 'user2@nyu.edu', 'credit', '1111-2222-3333-5555', 'Cathy Wood', '2025-03-30', '2024-02-04', '11:55:55'),
('4', 'user1@nyu.edu', 'credit', '1111-2222-3333-5555', 'Alice Bob', '2025-03-30', '2024-01-21', '11:55:55'),
('5', 'testcustomer@nyu.edu', 'credit', '1111-2222-3333-4444', 'Jon Snow', '2024-03-30', '2024-02-28', '11:55:55'),
('6', 'testcustomer@nyu.edu', 'credit', '1111-2222-3333-4444', 'Jon Snow', '2024-03-30', '2024-01-02', '11:55:55'),
('7', 'user3@nyu.edu', 'credit', '1111-2222-3333-5555', 'Trudy Jones', '2024-03-30', '2023-12-03', '11:55:55'),
('8', 'user3@nyu.edu', 'credit', '1111-2222-3333-5555', 'Trudy Jones', '2024-03-30', '2023-05-23', '11:55:55'),
('9', 'user3@nyu.edu', 'credit', '1111-2222-3333-5555', 'Trudy Jones', '2024-03-30', '2023-12-04', '11:55:55'),
('11', 'user3@nyu.edu', 'credit', '1111-2222-3333-5555', 'Trudy Jones', '2024-03-30', '2023-10-23', '11:55:55'),
('12', 'testcustomer@nyu.edu', 'credit', '1111-2222-3333-4444', 'Jon Snow', '2024-03-30', '2023-10-02', '11:55:55'),
('14', 'user3@nyu.edu', 'credit', '1111-2222-3333-5555', 'Trudy Jones', '2024-03-30', '2024-04-20', '11:55:55'),
('15', 'user1@nyu.edu', 'credit', '1111-2222-3333-5555', 'Alice Bob', '2024-03-30', '2024-04-21', '11:55:55'),
('16', 'user2@nyu.edu', 'credit', '1111-2222-3333-5555', 'Cathy Wood', '2024-03-30', '2024-02-19', '11:55:55'),
('17', 'user1@nyu.edu', 'credit', '1111-2222-3333-5555', 'Alice Bob', '2024-03-30', '2024-01-11', '11:55:55'),
('18', 'testcustomer@nyu.edu', 'credit', '1111-2222-3333-4444', 'Jon Snow', '2024-03-30', '2024-02-25', '11:55:55'),
('19', 'user1@nyu.edu', 'credit', '1111-2222-3333-4444', 'Alice Bob', '2024-03-30', '2024-04-22', '11:55:55'),
('20', 'testcustomer@nyu.edu', 'credit', '1111-2222-3333-4444', 'Jon Snow', '2024-03-30', '2023-12-12', '11:55:55');

-- --------------------------------------------------------

--
-- Table structure for table `creates`
--

CREATE TABLE `creates` (
  `airline_name` varchar(255) NOT NULL,
  `flight_number` int(11) NOT NULL,
  `departure_date` date NOT NULL,
  `departure_time` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `creates`
--

INSERT INTO `creates` (`airline_name`, `flight_number`, `departure_date`, `departure_time`) VALUES
('United', 296, '2024-05-30', '13:25:25'),
('United', 715, '2024-02-28', '10:25:25'),
('United', 206, '2024-07-04', '13:25:25'),
('United', 207, '2024-08-04', '13:25:25'),
('United', 102, '2024-02-12', '13:25:25'),
('United', 104, '2024-03-04', '13:25:25'),
('United', 106, '2024-01-04', '13:25:25'),
('United', 134, '2024-12-12', '13:25:25'),
('United', 839, '2023-05-26', '13:25:25');

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `primary_phone` varchar(15) NOT NULL,
  `building_number` int(11) NOT NULL,
  `street_name` varchar(255) NOT NULL,
  `apartment_number` int(11) DEFAULT NULL,
  `city` varchar(255) NOT NULL,
  `state` varchar(255) NOT NULL,
  `zip_code` int(11) NOT NULL,
  `passport_number` int(11) NOT NULL,
  `passport_expiration` date NOT NULL,
  `passport_country` varchar(255) NOT NULL,
  `date_of_birth` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`email`, `password`, `first_name`, `last_name`, `primary_phone`, `building_number`, `street_name`, `apartment_number`, `city`, `state`, `zip_code`, `passport_number`, `passport_expiration`, `passport_country`, `date_of_birth`) VALUES
('testcustomer@nyu.edu', '$2b$12$5kZPWupXtX5g6aC5uqmmeeKE34DO1LDYmTZ2rIi3J0GpcMhXZIbfG', 'Jon', 'Snow', '123-4321- 4321', 1555, 'Jay St', NULL, 'Brooklyn', 'New York', 11225, 54321, '2025-12-24', 'USA', '1999-01-19'),
('user1@nyu.edu', '$2b$12$Jum15ndBXJ.KMxSRe9KisuWOESvHkU50K3cOK9FzXGyPuCyXA1swq', 'Alice', 'Bob', '123-4322-4322', 5405, 'Jay Street', NULL, 'Brooklyn', 'New York', 11201, 54322, '2025-12-25', 'USA', '1999-11-19'),
('user2@nyu.edu', '$2b$12$.TW2FIMeL8O7cZxZnhtbvueBKXrDr0IM4PffiMQQsKvYPabl657PG', 'Cathy', 'Wood', '123-4323- 4323', 1702, 'Jay Street', NULL, 'Brooklyn', 'New York', 11201, 54323, '2025-10-24', 'USA', '1999-10-19'),
('user3@nyu.edu', '$2b$12$ONQbDDDSR1tpTu21SchgYOMRFLlynOE1axxOkEGL.1vx6.VVeYNEu', 'Trudy', 'Jones', '123-4324- 4324', 1890, 'Jay Street', NULL, 'Brooklyn', 'New York', 11201, 54324, '2025-09-24', 'USA', '1999-09-19');

-- --------------------------------------------------------

--
-- Table structure for table `flight`
--

CREATE TABLE `flight` (
  `flight_number` int(11) NOT NULL,
  `departure_date` date NOT NULL,
  `departure_time` time NOT NULL,
  `airplane_id` varchar(255) NOT NULL,
  `departure_airport` varchar(255) DEFAULT NULL,
  `arrival_date` date NOT NULL,
  `arrival_time` time NOT NULL,
  `arrival_airport` varchar(255) DEFAULT NULL,
  `ticket_price` decimal(65,2) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `empty_seats` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `flight`
--

INSERT INTO `flight` (`flight_number`, `departure_date`, `departure_time`, `airplane_id`, `departure_airport`, `arrival_date`, `arrival_time`, `arrival_airport`, `ticket_price`, `status`, `empty_seats`) VALUES
(102, '2024-02-12', '13:25:25', '3', 'SFO', '2024-02-12', '16:50:25', 'LAX', 300.00, 'On-Time', '50'),
(104, '2024-03-04', '13:25:25', '3', 'PVG', '2024-03-04', '16:50:25', 'BEI', 300.00, 'On-Time', '50'),
(106, '2024-01-04', '13:25:25', '3', 'SFO', '2024-01-04', '16:50:25', 'LAX', 350.00, 'Delayed', '50'),
(134, '2024-12-12', '13:25:25', '3', 'JFK', '2024-12-12', '16:50:25', 'BOS', 300.00, 'Delayed', '50'),
(206, '2024-07-04', '13:25:25', '2', 'SFO', '2024-07-04', '16:50:25', 'LAX', 400.00, 'On-Time', '4'),
(207, '2024-08-04', '13:25:25', '2', 'LAX', '2024-08-04', '16:50:25', 'SFO', 300.00, 'On-Time', '4'),
(296, '2024-05-30', '13:25:25', '1', 'PVG', '2024-05-30', '16:50:25', 'SFO', 3000.00, 'On-Time', '4'),
(715, '2024-02-28', '10:25:25', '1', 'PVG', '2024-02-28', '13:50:25', 'BEI', 500.00, 'Delayed', '4'),
(839, '2023-05-26', '13:25:25', '3', 'SHEN', '2023-05-26', '16:50:25', 'BEI', 300.00, 'On-Time', '50');

-- --------------------------------------------------------

--
-- Table structure for table `maintenance_procedure`
--

CREATE TABLE `maintenance_procedure` (
  `airplane_id` varchar(255) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `airline_name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `maintenance_procedure`
--

INSERT INTO `maintenance_procedure` (`airplane_id`, `start_date`, `end_date`, `start_time`, `end_time`, `airline_name`) VALUES
('1', '2024-06-27', '2024-06-29', '13:25:00', '07:25:00', 'United'),
('2', '2024-01-27', '2024-01-29', '13:25:25', '07:25:25', 'United');

-- --------------------------------------------------------

--
-- Table structure for table `rates`
--

CREATE TABLE `rates` (
  `email` varchar(255) NOT NULL,
  `flight_number` int(11) NOT NULL,
  `departure_date` date NOT NULL,
  `departure_time` time NOT NULL,
  `rating` int(11) NOT NULL,
  `comment` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `rates`
--

INSERT INTO `rates` (`email`, `flight_number`, `departure_date`, `departure_time`, `rating`, `comment`) VALUES
('user1@nyu.edu', 102, '2024-02-12', '13:25:25', 5, 'Relaxing, check-in and onboarding very professional'),
('user1@nyu.edu', 104, '2024-03-04', '13:25:25', 5, 'Comfortable journey and Professional'),
('testcustomer@nyu.edu', 102, '2024-02-12', '13:25:25', 4, 'Very Comfortable'),
('testcustomer@nyu.edu', 104, '2024-03-04', '13:25:25', 1, 'Customer Care services are not good'),
('user2@nyu.edu', 102, '2024-02-12', '13:25:25', 3, 'Relaxing, check-in and onboarding very professional');

-- --------------------------------------------------------

--
-- Table structure for table `secondary_customer_phone`
--

CREATE TABLE `secondary_customer_phone` (
  `email` varchar(255) NOT NULL,
  `phone_number` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `secondary_staff_email`
--

CREATE TABLE `secondary_staff_email` (
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `secondary_staff_phone`
--

CREATE TABLE `secondary_staff_phone` (
  `username` varchar(255) NOT NULL,
  `phone_number` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `secondary_staff_phone`
--

INSERT INTO `secondary_staff_phone` (`username`, `phone_number`) VALUES
('admin', '44455556666');

-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

CREATE TABLE `ticket` (
  `ticket_id` varchar(255) NOT NULL,
  `flight_number` int(11) NOT NULL,
  `departure_date` date NOT NULL,
  `departure_time` time NOT NULL,
  `email` varchar(255) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `date_of_birth` date NOT NULL,
  `current_price` decimal(65,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`ticket_id`, `flight_number`, `departure_date`, `departure_time`, `email`, `first_name`, `last_name`, `date_of_birth`, `current_price`) VALUES
('1', 102, '2024-02-12', '13:25:25', 'testcustomer@nyu.edu', 'Jon', 'Snow', '1999-12-19', 300.00),
('11', 134, '2024-12-12', '13:25:25', 'user3@nyu.edu', 'Trudy', 'Jones', '1999-09-19', 300.00),
('12', 715, '2024-02-28', '10:25:25', 'testcustomer@nyu.edu', 'Jon', 'Snow', '1999-12-19', 500.00),
('14', 206, '2024-07-04', '13:25:25', 'user3@nyu.edu', 'Trudy', 'Jones', '1999-09-19', 400.00),
('15', 206, '2024-07-04', '13:25:25', 'user1@nyu.edu', 'Alice', 'Bob', '1999-11-19', 400.00),
('16', 206, '2024-07-04', '13:25:25', 'user2@nyu.edu', 'Cathy', 'Wood', '1999-10-19', 400.00),
('17', 207, '2024-08-04', '13:25:25', 'user1@nyu.edu', 'Alice', 'Bob', '1999-11-19', 300.00),
('18', 207, '2024-08-04', '13:25:25', 'testcustomer@nyu.edu', 'Jon', 'Snow', '1999-12-19', 300.00),
('19', 296, '2024-05-30', '13:25:25', 'user1@nyu.edu', 'Alice', 'Bob', '1999-11-19', 3000.00),
('2', 102, '2024-02-12', '13:25:25', 'user1@nyu.edu', 'Alice', 'Bob', '1999-11-19', 300.00),
('20', 296, '2024-05-30', '13:25:25', 'user1@nyu.edu', 'Jon', 'Snow', '1999-12-19', 3000.00),
('3', 102, '2024-02-12', '13:25:25', 'user1@nyu.edu', 'Cathy', 'Wood', '1999-10-19', 300.00),
('4', 104, '2024-03-04', '13:25:25', 'user1@nyu.edu', 'Alice', 'Bob', '1999-11-19', 300.00),
('5', 104, '2024-03-04', '13:25:25', 'user1@nyu.edu', 'Jon', 'Snow', '1999-12-19', 300.00),
('6', 106, '2024-01-04', '13:25:25', 'user1@nyu.edu', 'Jon', 'Snow', '1999-12-19', 350.00),
('7', 106, '2024-01-04', '13:25:25', 'user3@nyu.edu', 'Trudy', 'Jones', '1999-09-19', 350.00),
('8', 839, '2023-05-26', '13:25:25', 'user3@nyu.edu', 'Trudy', 'Jones', '1999-09-19', 300.00),
('9', 102, '2024-02-12', '13:25:25', 'user3@nyu.edu', 'Trudy', 'Jones', '1999-09-19', 300.00);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `airline`
--
ALTER TABLE `airline`
  ADD PRIMARY KEY (`name`);

--
-- Indexes for table `airline_staff`
--
ALTER TABLE `airline_staff`
  ADD PRIMARY KEY (`username`),
  ADD KEY `airline_name` (`airline_name`);

--
-- Indexes for table `airplane`
--
ALTER TABLE `airplane`
  ADD PRIMARY KEY (`airplane_id`,`airline_name`),
  ADD KEY `airline_name` (`airline_name`);

--
-- Indexes for table `airport`
--
ALTER TABLE `airport`
  ADD PRIMARY KEY (`code`);

--
-- Indexes for table `buys`
--
ALTER TABLE `buys`
  ADD KEY `ticket_id` (`ticket_id`),
  ADD KEY `email` (`email`);

--
-- Indexes for table `creates`
--
ALTER TABLE `creates`
  ADD KEY `airline_name` (`airline_name`),
  ADD KEY `flight_number` (`flight_number`,`departure_date`,`departure_time`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `flight`
--
ALTER TABLE `flight`
  ADD PRIMARY KEY (`flight_number`,`departure_date`,`departure_time`),
  ADD KEY `airplane_id` (`airplane_id`);

--
-- Indexes for table `maintenance_procedure`
--
ALTER TABLE `maintenance_procedure`
  ADD KEY `airplane_id` (`airplane_id`),
  ADD KEY `fk_airline` (`airline_name`);

--
-- Indexes for table `rates`
--
ALTER TABLE `rates`
  ADD KEY `flight_number` (`flight_number`,`departure_date`,`departure_time`),
  ADD KEY `email` (`email`);

--
-- Indexes for table `secondary_customer_phone`
--
ALTER TABLE `secondary_customer_phone`
  ADD KEY `email` (`email`);

--
-- Indexes for table `secondary_staff_email`
--
ALTER TABLE `secondary_staff_email`
  ADD KEY `username` (`username`);

--
-- Indexes for table `secondary_staff_phone`
--
ALTER TABLE `secondary_staff_phone`
  ADD KEY `username` (`username`);

--
-- Indexes for table `ticket`
--
ALTER TABLE `ticket`
  ADD PRIMARY KEY (`ticket_id`),
  ADD KEY `flight_number` (`flight_number`,`departure_date`,`departure_time`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `airline_staff`
--
ALTER TABLE `airline_staff`
  ADD CONSTRAINT `airline_staff_ibfk_1` FOREIGN KEY (`airline_name`) REFERENCES `airline` (`name`);

--
-- Constraints for table `airplane`
--
ALTER TABLE `airplane`
  ADD CONSTRAINT `airplane_ibfk_1` FOREIGN KEY (`airline_name`) REFERENCES `airline` (`name`) ON DELETE CASCADE;

--
-- Constraints for table `buys`
--
ALTER TABLE `buys`
  ADD CONSTRAINT `buys_ibfk_1` FOREIGN KEY (`ticket_id`) REFERENCES `ticket` (`ticket_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `buys_ibfk_2` FOREIGN KEY (`email`) REFERENCES `customer` (`email`);

--
-- Constraints for table `creates`
--
ALTER TABLE `creates`
  ADD CONSTRAINT `creates_ibfk_1` FOREIGN KEY (`airline_name`) REFERENCES `airline` (`name`),
  ADD CONSTRAINT `creates_ibfk_2` FOREIGN KEY (`flight_number`,`departure_date`,`departure_time`) REFERENCES `flight` (`flight_number`, `departure_date`, `departure_time`);

--
-- Constraints for table `flight`
--
ALTER TABLE `flight`
  ADD CONSTRAINT `flight_ibfk_1` FOREIGN KEY (`airplane_id`) REFERENCES `airplane` (`airplane_id`);

--
-- Constraints for table `maintenance_procedure`
--
ALTER TABLE `maintenance_procedure`
  ADD CONSTRAINT `fk_airline` FOREIGN KEY (`airline_name`) REFERENCES `airplane` (`airline_name`),
  ADD CONSTRAINT `maintenance_procedure_ibfk_1` FOREIGN KEY (`airplane_id`) REFERENCES `airplane` (`airplane_id`) ON DELETE CASCADE;

--
-- Constraints for table `rates`
--
ALTER TABLE `rates`
  ADD CONSTRAINT `rates_ibfk_1` FOREIGN KEY (`flight_number`,`departure_date`,`departure_time`) REFERENCES `flight` (`flight_number`, `departure_date`, `departure_time`),
  ADD CONSTRAINT `rates_ibfk_2` FOREIGN KEY (`email`) REFERENCES `customer` (`email`);

--
-- Constraints for table `secondary_customer_phone`
--
ALTER TABLE `secondary_customer_phone`
  ADD CONSTRAINT `secondary_customer_phone_ibfk_1` FOREIGN KEY (`email`) REFERENCES `customer` (`email`) ON DELETE CASCADE;

--
-- Constraints for table `secondary_staff_email`
--
ALTER TABLE `secondary_staff_email`
  ADD CONSTRAINT `secondary_staff_email_ibfk_1` FOREIGN KEY (`username`) REFERENCES `airline_staff` (`username`) ON DELETE CASCADE;

--
-- Constraints for table `secondary_staff_phone`
--
ALTER TABLE `secondary_staff_phone`
  ADD CONSTRAINT `secondary_staff_phone_ibfk_1` FOREIGN KEY (`username`) REFERENCES `airline_staff` (`username`) ON DELETE CASCADE;

--
-- Constraints for table `ticket`
--
ALTER TABLE `ticket`
  ADD CONSTRAINT `ticket_ibfk_1` FOREIGN KEY (`flight_number`,`departure_date`,`departure_time`) REFERENCES `flight` (`flight_number`, `departure_date`, `departure_time`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
