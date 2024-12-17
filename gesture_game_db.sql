-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 28-11-2024 a las 02:56:43
-- Versión del servidor: 10.4.22-MariaDB
-- Versión de PHP: 8.1.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `gesture_game_db`
--

DELIMITER $$
--
-- Procedimientos
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `ObtenerEstadisticasUsuario` (IN `p_usuario_id` INT)  BEGIN
    SELECT 
        COUNT(*) AS total_partidas,
        COALESCE(AVG(puntuacion), 0) AS promedio_puntuacion,
        COALESCE(MAX(puntuacion), 0) AS maximo_puntaje,
        COALESCE(MIN(puntuacion), 0) AS minimo_puntaje
    FROM partidas
    WHERE usuario_id = p_usuario_id;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `partidas`
--

CREATE TABLE `partidas` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `puntuacion` int(11) NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `partidas`
--

INSERT INTO `partidas` (`id`, `usuario_id`, `puntuacion`, `fecha`) VALUES
(1, 3, 0, '2024-11-26 05:42:25'),
(2, 3, 0, '2024-11-26 05:44:57'),
(3, 2, 0, '2024-11-26 05:47:46'),
(4, 2, 0, '2024-11-26 05:48:16'),
(5, 2, 0, '2024-11-26 05:48:22'),
(6, 2, 0, '2024-11-26 05:48:26'),
(7, 2, 0, '2024-11-26 05:48:28'),
(8, 2, 0, '2024-11-26 05:59:15'),
(9, 2, 1, '2024-11-26 06:07:02'),
(10, 2, 0, '2024-11-26 06:17:04'),
(11, 4, 2, '2024-11-26 06:31:31'),
(12, 2, 2, '2024-11-26 06:52:30'),
(13, 2, 0, '2024-11-26 07:28:24'),
(14, 2, 4, '2024-11-26 08:33:18'),
(15, 2, 35, '2024-11-26 08:35:17'),
(16, 2, 23, '2024-11-26 08:44:33'),
(17, 2, 28, '2024-11-26 08:51:26'),
(18, 2, 30, '2024-11-26 08:54:25'),
(19, 2, 28, '2024-11-26 08:54:25'),
(20, 2, 18, '2024-11-26 08:54:25'),
(21, 2, 5, '2024-11-26 09:02:52'),
(22, 2, 0, '2024-11-26 14:01:09'),
(23, 2, 17, '2024-11-26 15:21:58'),
(24, 2, 19, '2024-11-28 00:01:55'),
(25, 3, 10, '2024-11-25 06:00:00'),
(26, 3, 15, '2024-11-25 06:00:00'),
(27, 3, 28, '2024-11-25 06:00:00'),
(28, 3, 35, '2024-11-25 06:00:00'),
(29, 3, 32, '2024-11-25 06:00:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(64) NOT NULL,
  `fecha_registro` timestamp NOT NULL DEFAULT current_timestamp(),
  `es_admin` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `username`, `email`, `password`, `fecha_registro`, `es_admin`) VALUES
(1, 'prueba', 'prueba@example.com', '8bb0cf6eb9b17d0f7d22b456f121257dc1254e1f01665370476383ea776df414', '2024-11-26 01:41:55', 0),
(2, 'Fatima', 'fatymamedyna@gmail.com', 'b304cf69e875423a6aa689b50bf60f4eb5b89fb18e3d8d1e02f70585fb6df122', '2024-11-26 01:48:42', 0),
(3, 'janeth', 'janeth@gmail.com', '75719042ce2fb91c658e2eb894a1e8b4aa57fc48a4ed15561b089843c1e0df1d', '2024-11-26 05:41:42', 0),
(4, 'Angeles', 'Angeles22@gmail.com', '17756315ebd47b7110359fc7b168179bf6f2df3646fcc888bc8aa05c78b38ac1', '2024-11-26 06:29:30', 0),
(6, 'admin', 'admin@example.com', '41e5653fc7aeb894026d6bb7b2db7f65902b454945fa8fd65a6327047b5277fb', '2024-11-28 00:40:21', 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `partidas`
--
ALTER TABLE `partidas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_usuario_partidas` (`usuario_id`),
  ADD KEY `idx_fecha_partidas` (`fecha`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `partidas`
--
ALTER TABLE `partidas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `partidas`
--
ALTER TABLE `partidas`
  ADD CONSTRAINT `partidas_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
