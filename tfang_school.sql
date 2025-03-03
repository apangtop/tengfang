/*
 Navicat MySQL Data Transfer

 Source Server         : Mysql8
 Source Server Type    : MySQL
 Source Server Version : 80035
 Source Host           : localhost:3307
 Source Schema         : tfang_school

 Target Server Type    : MySQL
 Target Server Version : 80035
 File Encoding         : 65001

 Date: 01/03/2025 23:05:37
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_group
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`(`group_id`, `permission_id`) USING BTREE,
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq`(`content_type_id`, `codename`) USING BTREE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 36 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO `auth_permission` VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO `auth_permission` VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO `auth_permission` VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO `auth_permission` VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO `auth_permission` VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO `auth_permission` VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO `auth_permission` VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO `auth_permission` VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO `auth_permission` VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO `auth_permission` VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO `auth_permission` VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO `auth_permission` VALUES (13, 'Can add user', 4, 'add_user');
INSERT INTO `auth_permission` VALUES (14, 'Can change user', 4, 'change_user');
INSERT INTO `auth_permission` VALUES (15, 'Can delete user', 4, 'delete_user');
INSERT INTO `auth_permission` VALUES (16, 'Can view user', 4, 'view_user');
INSERT INTO `auth_permission` VALUES (17, 'Can add content type', 5, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (18, 'Can change content type', 5, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (19, 'Can delete content type', 5, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (20, 'Can view content type', 5, 'view_contenttype');
INSERT INTO `auth_permission` VALUES (21, 'Can add session', 6, 'add_session');
INSERT INTO `auth_permission` VALUES (22, 'Can change session', 6, 'change_session');
INSERT INTO `auth_permission` VALUES (23, 'Can delete session', 6, 'delete_session');
INSERT INTO `auth_permission` VALUES (24, 'Can view session', 6, 'view_session');
INSERT INTO `auth_permission` VALUES (25, 'Can add 系统配置', 7, 'add_systemconfig');
INSERT INTO `auth_permission` VALUES (26, 'Can change 系统配置', 7, 'change_systemconfig');
INSERT INTO `auth_permission` VALUES (27, 'Can delete 系统配置', 7, 'delete_systemconfig');
INSERT INTO `auth_permission` VALUES (28, 'Can view 系统配置', 7, 'view_systemconfig');
INSERT INTO `auth_permission` VALUES (29, 'Can add 节目类别', 8, 'add_programcategory');
INSERT INTO `auth_permission` VALUES (30, 'Can change 节目类别', 8, 'change_programcategory');
INSERT INTO `auth_permission` VALUES (31, 'Can delete 节目类别', 8, 'delete_programcategory');
INSERT INTO `auth_permission` VALUES (32, 'Can view 节目类别', 8, 'view_programcategory');
INSERT INTO `auth_permission` VALUES (33, 'Can add 节目', 9, 'add_program');
INSERT INTO `auth_permission` VALUES (34, 'Can change 节目', 9, 'change_program');
INSERT INTO `auth_permission` VALUES (35, 'Can delete 节目', 9, 'delete_program');
INSERT INTO `auth_permission` VALUES (36, 'Can view 节目', 9, 'view_program');

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) NULL DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user
-- ----------------------------
INSERT INTO `auth_user` VALUES (1, 'pbkdf2_sha256$870000$VvYBBgBr1lbvEdrxAHJeQy$vMIIAlh6NoVtKJRhlJXgafMwFrbF4PZ2TutVnyAU8VE=', '2025-02-28 01:50:12.207734', 1, 'admin', '', '', '771154265@qq.com', 1, 1, '2025-02-28 01:49:36.486154');

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_groups_user_id_group_id_94350c0c_uniq`(`user_id`, `group_id`) USING BTREE,
  INDEX `auth_user_groups_group_id_97559544_fk_auth_group_id`(`group_id`) USING BTREE,
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user_groups
-- ----------------------------

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq`(`user_id`, `permission_id`) USING BTREE,
  INDEX `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user_user_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for broadcast_program
-- ----------------------------
DROP TABLE IF EXISTS `broadcast_program`;
CREATE TABLE `broadcast_program`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `publish_date` date NOT NULL,
  `link` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `category_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `broadcast_program_category_id_9a162df1_fk_broadcast`(`category_id`) USING BTREE,
  CONSTRAINT `broadcast_program_category_id_9a162df1_fk_broadcast` FOREIGN KEY (`category_id`) REFERENCES `broadcast_programcategory` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 25 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of broadcast_program
-- ----------------------------
INSERT INTO `broadcast_program` VALUES (1, '《宗师列传·唐宋八大家》 20231110 韩愈·上', '2025-02-28', 'https://tv.cctv.com/2023/12/17/VIDEufQ3133GnTDYxbqFp7sE231217.shtml?spm=C55953877151.PnBseTLNFz7W.0.0', 1, 4);
INSERT INTO `broadcast_program` VALUES (2, '《宗师列传·唐宋八大家》 20231117 韩愈·下', '2025-02-28', 'https://tv.cctv.com/2023/11/17/VIDE1KzYiSQerv2aL5sCrk9E231117.shtml?spm=C55953877151.PnBseTLNFz7W.0.0', 1, 4);
INSERT INTO `broadcast_program` VALUES (3, '《宗师列传·唐宋八大家》 20231208 欧阳修·上', '2025-02-28', 'https://tv.cctv.com/2023/12/27/VIDEIy5J03uSsQxp7NrarmI2231227.shtml?spm=C55953877151.PnBseTLNFz7W.0.0', 1, 4);
INSERT INTO `broadcast_program` VALUES (4, '《宗师列传·唐宋八大家》 20231215 欧阳修·下', '2025-02-28', 'https://tv.cctv.com/2023/12/15/VIDEdYNtCYNq1uBMKryA4xJH231215.shtml?spm=C55953877151.PnBseTLNFz7W.0.0', 1, 4);
INSERT INTO `broadcast_program` VALUES (5, '《宗师列传·唐宋八大家》 20231201 柳宗元', '2025-02-28', 'https://tv.cctv.com/2024/01/05/VIDEbtQAk764B5RwsSFYpSdt240105.shtml?spm=C55953877151.PnBseTLNFz7W.0.0', 1, 4);
INSERT INTO `broadcast_program` VALUES (6, '宗师列传·唐宋八大家》 20231229 苏洵', '2025-02-28', 'https://tv.cctv.com/2024/01/05/VIDEiZ1lWQjX21s6DDx30J2r240105.shtml?spm=C55953877151.PnBseTLNFz7W.0.0', 1, 4);
INSERT INTO `broadcast_program` VALUES (7, '《宗师列传·唐宋八大家》 20240105 苏轼 苏辙·上', '2025-02-28', 'https://tv.cctv.com/2024/01/21/VIDEr4YmmqNgIIm5hX0LBDw8240121.shtml?spm=C55953877151.PnBseTLNFz7W.0.0', 1, 4);
INSERT INTO `broadcast_program` VALUES (8, '《宗师列传·唐宋八大家》 20240119 苏轼 苏辙·中', '2025-02-28', 'https://tv.cctv.com/2024/01/24/VIDEMJbEoHHAdq5SF7CFpNJq240124.shtml?spm=C55953877151.PnBseTLNFz7W.0.0', 1, 4);
INSERT INTO `broadcast_program` VALUES (9, '《宗师列传·唐宋八大家》 20240126 苏轼 苏辙·下', '2025-02-28', 'https://tv.cctv.com/2024/01/28/VIDECQtL9QVgnNkheEqeDupK240128.shtml?spm=C55953877151.PnBseTLNFz7W.0.0', 1, 4);
INSERT INTO `broadcast_program` VALUES (10, '《宗师列传·唐宋八大家》 20240302 王安石', '2025-02-28', 'https://tv.cctv.com/2024/03/02/VIDEgxMk2vxcOmMK9ROgRgRa240302.shtml?spm=C55953877151.PnBseTLNFz7W.0.0', 1, 4);
INSERT INTO `broadcast_program` VALUES (11, '《宗师列传·唐宋八大家》 20240302 王安石', '2025-02-28', 'https://tv.cctv.com/2024/03/02/VIDEgxMk2vxcOmMK9ROgRgRa240302.shtml?spm=C55953877151.PnBseTLNFz7W.0.0', 1, 4);
INSERT INTO `broadcast_program` VALUES (12, '《宗师列传·唐宋八大家》 20240308 曾巩', '2025-02-28', 'https://tv.cctv.com/2024/03/08/VIDENufBd8N1P6LBCtsGrirN240308.shtml?spm=C55953877151.PnBseTLNFz7W.0.0', 1, 4);
INSERT INTO `broadcast_program` VALUES (13, '《宗师列传·唐宋八大家》 20240515 柳宗元', '2025-02-28', 'https://tv.cctv.com/2024/05/16/VIDE613Gl1a5tEebWHxi4O9k240516.shtml?spm=C55953877151.PnBseTLNFz7W.0.0', 1, 4);
INSERT INTO `broadcast_program` VALUES (14, '《新闻周刊》 20250222', '2025-02-24', 'https://tv.cctv.com/2025/02/23/VIDEQpHVOtDXbHv7spuNN0SA250223.shtml', 1, 1);
INSERT INTO `broadcast_program` VALUES (15, '《今日说法》 20250226 “守护劳动者”系列报道 上班途中', '2025-02-25', 'https://tv.cctv.com/2025/02/26/VIDEjXjIL9vZBzWUycMpNNRM250226.shtml', 1, 3);
INSERT INTO `broadcast_program` VALUES (16, '《宗师列传·大唐诗人传》 20241101 初唐四杰', '2025-03-01', 'https://tv.cctv.com/2024/11/01/VIDEnYcZQtB5jYvWnorC4k0r241101.shtml?spm=C55953877151.PnBseTLNFz7W.0.', 1, 5);
INSERT INTO `broadcast_program` VALUES (17, '《宗师列传·大唐诗人传》 20241102 孟浩然', '2025-03-01', 'https://tv.cctv.com/2024/11/02/VIDEyw24P7r5i3Ij4l8MD1oK241102.shtml?spm=C55953877151.PnBseTLNFz7W.0.0', 1, 5);
INSERT INTO `broadcast_program` VALUES (18, '《宗师列传·大唐诗人传》 20241109 王昌龄', '2025-03-01', 'https://tv.cctv.com/2024/11/09/VIDEVKGEqqmaeEzo22ziUJyI241109.shtml?spm=C55953877151.PnBseTLNFz7W.0.0', 1, 5);
INSERT INTO `broadcast_program` VALUES (19, '《宗师列传·大唐诗人传》 20241116 王维', '2025-03-01', 'https://tv.cctv.com/2024/11/16/VIDEhVZeWU1OpegGFo9BmQng241116.shtml?spm=C55953877151.PnBseTLNFz7W.0.0', 1, 5);
INSERT INTO `broadcast_program` VALUES (20, '《宗师列传·大唐诗人传》 20241123 李白', '2025-03-01', 'https://tv.cctv.com/2024/11/23/VIDEpPIoOV3u0rzhWb6P0Mkb241123.shtml?spm=C55953877151.PnBseTLNFz7W.0.0', 1, 5);
INSERT INTO `broadcast_program` VALUES (21, '《宗师列传·大唐诗人传》 20241130 杜甫', '2025-03-01', 'https://tv.cctv.com/2024/11/30/VIDErn22KTqIts2ScBUMs7W9241130.shtml?spm=C55953877151.PnBseTLNFz7W.0.0', 1, 5);
INSERT INTO `broadcast_program` VALUES (22, '《宗师列传·大唐诗人传》 20241214 岑参', '2025-03-01', 'https://tv.cctv.com/2024/12/14/VIDEcKFKZSA6fyE1w9gCtGLm241214.shtml?spm=C55953877151.PnBseTLNFz7W.0.0', 1, 5);
INSERT INTO `broadcast_program` VALUES (23, '《宗师列传·大唐诗人传》 20241227 白居易', '2025-03-01', 'https://tv.cctv.com/2024/12/27/VIDEoPRFfWRZnjoPMpdgA3CI241227.shtml?spm=C55953877151.PnBseTLNFz7W.0.0', 1, 5);
INSERT INTO `broadcast_program` VALUES (24, '《宗师列传·大唐诗人传》 20250111 李贺', '2025-03-01', 'https://tv.cctv.com/2025/01/11/VIDEJbZzQwhdFMU6tWIeJHbb250111.shtml?spm=C55953877151.PnBseTLNFz7W.0.0', 1, 5);

-- ----------------------------
-- Table structure for broadcast_programcategory
-- ----------------------------
DROP TABLE IF EXISTS `broadcast_programcategory`;
CREATE TABLE `broadcast_programcategory`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `day_of_week` int NOT NULL,
  `icon_class` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `color` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_biweekly` tinyint(1) NOT NULL,
  `alternate_with_id` bigint NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `broadcast_programcat_alternate_with_id_698d794b_fk_broadcast`(`alternate_with_id`) USING BTREE,
  CONSTRAINT `broadcast_programcat_alternate_with_id_698d794b_fk_broadcast` FOREIGN KEY (`alternate_with_id`) REFERENCES `broadcast_programcategory` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of broadcast_programcategory
-- ----------------------------
INSERT INTO `broadcast_programcategory` VALUES (1, '新闻周刊', '', 1, 'fa-newspaper', 'blue', 0, NULL);
INSERT INTO `broadcast_programcategory` VALUES (2, '世界周刊', '', 2, 'fa-newspaper', 'green', 1, 3);
INSERT INTO `broadcast_programcategory` VALUES (3, '今日说法', '', 2, 'fa-newspaper', 'green', 1, 2);
INSERT INTO `broadcast_programcategory` VALUES (4, '唐宋八大家', '', 4, 'fa-newspaper', 'pink', 0, NULL);
INSERT INTO `broadcast_programcategory` VALUES (5, '大唐诗人传', '', 4, 'fa-feather', 'amber', 0, NULL);

-- ----------------------------
-- Table structure for broadcast_systemconfig
-- ----------------------------
DROP TABLE IF EXISTS `broadcast_systemconfig`;
CREATE TABLE `broadcast_systemconfig`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `first_week_start_date` date NOT NULL,
  `semester_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of broadcast_systemconfig
-- ----------------------------
INSERT INTO `broadcast_systemconfig` VALUES (1, '2025-02-17', '2025年春季学期', '2025-02-28 01:54:59.226923', '2025-02-28 01:55:02.002655');

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `object_repr` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NULL DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co`(`content_type_id`) USING BTREE,
  INDEX `django_admin_log_user_id_c564eba6_fk_auth_user_id`(`user_id`) USING BTREE,
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 42 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------
INSERT INTO `django_admin_log` VALUES (1, '2025-02-28 01:54:59.227916', '1', '2025年春季学期 - 起始日期: 2025-02-17', 1, '[{\"added\": {}}]', 7, 1);
INSERT INTO `django_admin_log` VALUES (2, '2025-02-28 01:55:02.003652', '1', '2025年春季学期 - 起始日期: 2025-02-17', 2, '[]', 7, 1);
INSERT INTO `django_admin_log` VALUES (3, '2025-02-28 02:12:41.049670', '1', '新闻周刊', 1, '[{\"added\": {}}]', 8, 1);
INSERT INTO `django_admin_log` VALUES (4, '2025-02-28 02:12:56.770021', '2', '世界周刊', 1, '[{\"added\": {}}]', 8, 1);
INSERT INTO `django_admin_log` VALUES (5, '2025-02-28 02:13:08.999394', '3', '今日说法', 1, '[{\"added\": {}}]', 8, 1);
INSERT INTO `django_admin_log` VALUES (6, '2025-02-28 02:13:31.843914', '2', '世界周刊', 2, '[{\"changed\": {\"fields\": [\"\\u8f6e\\u66ff\\u8282\\u76ee\"]}}]', 8, 1);
INSERT INTO `django_admin_log` VALUES (7, '2025-02-28 02:13:40.974580', '4', '唐宋八大家', 1, '[{\"added\": {}}]', 8, 1);
INSERT INTO `django_admin_log` VALUES (8, '2025-02-28 02:14:31.435495', '1', '《宗师列传·唐宋八大家》 20231110 韩愈·上', 1, '[{\"added\": {}}]', 9, 1);
INSERT INTO `django_admin_log` VALUES (9, '2025-02-28 02:14:47.863154', '2', '《宗师列传·唐宋八大家》 20231117 韩愈·下', 1, '[{\"added\": {}}]', 9, 1);
INSERT INTO `django_admin_log` VALUES (10, '2025-02-28 02:15:15.352113', '3', '《宗师列传·唐宋八大家》 20231208 欧阳修·上', 1, '[{\"added\": {}}]', 9, 1);
INSERT INTO `django_admin_log` VALUES (11, '2025-02-28 02:15:30.252783', '4', '《宗师列传·唐宋八大家》 20231215 欧阳修·下', 1, '[{\"added\": {}}]', 9, 1);
INSERT INTO `django_admin_log` VALUES (12, '2025-02-28 02:15:48.185648', '5', '《宗师列传·唐宋八大家》 20231201 柳宗元', 1, '[{\"added\": {}}]', 9, 1);
INSERT INTO `django_admin_log` VALUES (13, '2025-02-28 02:16:03.694069', '6', '宗师列传·唐宋八大家》 20231229 苏洵', 1, '[{\"added\": {}}]', 9, 1);
INSERT INTO `django_admin_log` VALUES (14, '2025-02-28 02:16:25.327549', '7', '《宗师列传·唐宋八大家》 20240105 苏轼 苏辙·上', 1, '[{\"added\": {}}]', 9, 1);
INSERT INTO `django_admin_log` VALUES (15, '2025-02-28 02:16:48.082558', '8', '《宗师列传·唐宋八大家》 20240119 苏轼 苏辙·中', 1, '[{\"added\": {}}]', 9, 1);
INSERT INTO `django_admin_log` VALUES (16, '2025-02-28 02:17:06.218239', '9', '《宗师列传·唐宋八大家》 20240126 苏轼 苏辙·下', 1, '[{\"added\": {}}]', 9, 1);
INSERT INTO `django_admin_log` VALUES (17, '2025-02-28 02:17:48.525526', '10', '《宗师列传·唐宋八大家》 20240302 王安石', 1, '[{\"added\": {}}]', 9, 1);
INSERT INTO `django_admin_log` VALUES (18, '2025-02-28 02:18:30.086775', '11', '《宗师列传·唐宋八大家》 20240302 王安石', 1, '[{\"added\": {}}]', 9, 1);
INSERT INTO `django_admin_log` VALUES (19, '2025-02-28 02:18:53.653504', '12', '《宗师列传·唐宋八大家》 20240308 曾巩', 1, '[{\"added\": {}}]', 9, 1);
INSERT INTO `django_admin_log` VALUES (20, '2025-02-28 02:19:08.504327', '13', '《宗师列传·唐宋八大家》 20240515 柳宗元', 1, '[{\"added\": {}}]', 9, 1);
INSERT INTO `django_admin_log` VALUES (21, '2025-02-28 02:22:35.816860', '14', '《新闻周刊》 20250222', 1, '[{\"added\": {}}]', 9, 1);
INSERT INTO `django_admin_log` VALUES (22, '2025-02-28 02:23:41.477745', '15', '《今日说法》 20250226 “守护劳动者”系列报道 上班途中', 1, '[{\"added\": {}}]', 9, 1);
INSERT INTO `django_admin_log` VALUES (23, '2025-02-28 02:38:40.204430', '3', '今日说法', 2, '[{\"changed\": {\"fields\": [\"\\u4e3b\\u9898\\u989c\\u8272\"]}}]', 8, 1);
INSERT INTO `django_admin_log` VALUES (24, '2025-02-28 02:38:44.014239', '2', '世界周刊', 2, '[{\"changed\": {\"fields\": [\"\\u4e3b\\u9898\\u989c\\u8272\"]}}]', 8, 1);
INSERT INTO `django_admin_log` VALUES (25, '2025-02-28 02:39:00.300784', '4', '唐宋八大家', 2, '[{\"changed\": {\"fields\": [\"\\u4e3b\\u9898\\u989c\\u8272\"]}}]', 8, 1);
INSERT INTO `django_admin_log` VALUES (26, '2025-02-28 02:39:48.085482', '4', '唐宋八大家', 2, '[{\"changed\": {\"fields\": [\"\\u4e3b\\u9898\\u989c\\u8272\"]}}]', 8, 1);
INSERT INTO `django_admin_log` VALUES (27, '2025-02-28 02:40:08.756803', '4', '唐宋八大家', 2, '[{\"changed\": {\"fields\": [\"\\u4e3b\\u9898\\u989c\\u8272\"]}}]', 8, 1);
INSERT INTO `django_admin_log` VALUES (28, '2025-02-28 02:43:28.659780', '4', '唐宋八大家', 2, '[{\"changed\": {\"fields\": [\"\\u4e3b\\u9898\\u989c\\u8272\"]}}]', 8, 1);
INSERT INTO `django_admin_log` VALUES (29, '2025-02-28 02:43:47.251711', '4', '唐宋八大家', 2, '[{\"changed\": {\"fields\": [\"\\u4e3b\\u9898\\u989c\\u8272\"]}}]', 8, 1);
INSERT INTO `django_admin_log` VALUES (30, '2025-03-01 07:58:25.026685', '5', '大唐诗人传', 1, '[{\"added\": {}}]', 8, 1);
INSERT INTO `django_admin_log` VALUES (31, '2025-03-01 07:58:57.373431', '5', '大唐诗人传', 2, '[{\"changed\": {\"fields\": [\"\\u56fe\\u6807\\u7c7b\\u540d\", \"\\u4e3b\\u9898\\u989c\\u8272\"]}}]', 8, 1);
INSERT INTO `django_admin_log` VALUES (32, '2025-03-01 08:00:05.257858', '16', '《宗师列传·大唐诗人传》 20241101 初唐四杰', 1, '[{\"added\": {}}]', 9, 1);
INSERT INTO `django_admin_log` VALUES (33, '2025-03-01 08:01:19.987425', '17', '《宗师列传·大唐诗人传》 20241102 孟浩然', 1, '[{\"added\": {}}]', 9, 1);
INSERT INTO `django_admin_log` VALUES (34, '2025-03-01 08:01:35.281377', '18', '《宗师列传·大唐诗人传》 20241109 王昌龄', 1, '[{\"added\": {}}]', 9, 1);
INSERT INTO `django_admin_log` VALUES (35, '2025-03-01 08:01:48.525186', '19', '《宗师列传·大唐诗人传》 20241116 王维', 1, '[{\"added\": {}}]', 9, 1);
INSERT INTO `django_admin_log` VALUES (36, '2025-03-01 08:02:04.279484', '20', '《宗师列传·大唐诗人传》 20241123 李白', 1, '[{\"added\": {}}]', 9, 1);
INSERT INTO `django_admin_log` VALUES (37, '2025-03-01 08:02:19.073778', '21', '《宗师列传·大唐诗人传》 20241130 杜甫', 1, '[{\"added\": {}}]', 9, 1);
INSERT INTO `django_admin_log` VALUES (38, '2025-03-01 08:02:33.892280', '22', '《宗师列传·大唐诗人传》 20241214 岑参', 1, '[{\"added\": {}}]', 9, 1);
INSERT INTO `django_admin_log` VALUES (39, '2025-03-01 08:02:46.396546', '23', '《宗师列传·大唐诗人传》 20241227 白居易', 1, '[{\"added\": {}}]', 9, 1);
INSERT INTO `django_admin_log` VALUES (40, '2025-03-01 08:03:03.672230', '24', '《宗师列传·大唐诗人传》 20250111 李贺', 1, '[{\"added\": {}}]', 9, 1);
INSERT INTO `django_admin_log` VALUES (41, '2025-03-01 08:04:25.842793', '24', '《宗师列传·大唐诗人传》 20250111 李贺', 2, '[{\"changed\": {\"fields\": [\"\\u8282\\u76ee\\u7c7b\\u522b\"]}}]', 9, 1);

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq`(`app_label`, `model`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (4, 'auth', 'user');
INSERT INTO `django_content_type` VALUES (9, 'broadcast', 'program');
INSERT INTO `django_content_type` VALUES (8, 'broadcast', 'programcategory');
INSERT INTO `django_content_type` VALUES (7, 'broadcast', 'systemconfig');
INSERT INTO `django_content_type` VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (6, 'sessions', 'session');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 20 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES (1, 'contenttypes', '0001_initial', '2025-02-28 01:49:00.510337');
INSERT INTO `django_migrations` VALUES (2, 'auth', '0001_initial', '2025-02-28 01:49:00.809033');
INSERT INTO `django_migrations` VALUES (3, 'admin', '0001_initial', '2025-02-28 01:49:00.906970');
INSERT INTO `django_migrations` VALUES (4, 'admin', '0002_logentry_remove_auto_add', '2025-02-28 01:49:00.912955');
INSERT INTO `django_migrations` VALUES (5, 'admin', '0003_logentry_add_action_flag_choices', '2025-02-28 01:49:00.919461');
INSERT INTO `django_migrations` VALUES (6, 'contenttypes', '0002_remove_content_type_name', '2025-02-28 01:49:00.961317');
INSERT INTO `django_migrations` VALUES (7, 'auth', '0002_alter_permission_name_max_length', '2025-02-28 01:49:01.001316');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0003_alter_user_email_max_length', '2025-02-28 01:49:01.015860');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0004_alter_user_username_opts', '2025-02-28 01:49:01.020843');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0005_alter_user_last_login_null', '2025-02-28 01:49:01.048318');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0006_require_contenttypes_0002', '2025-02-28 01:49:01.049314');
INSERT INTO `django_migrations` VALUES (12, 'auth', '0007_alter_validators_add_error_messages', '2025-02-28 01:49:01.055298');
INSERT INTO `django_migrations` VALUES (13, 'auth', '0008_alter_user_username_max_length', '2025-02-28 01:49:01.088292');
INSERT INTO `django_migrations` VALUES (14, 'auth', '0009_alter_user_last_name_max_length', '2025-02-28 01:49:01.120729');
INSERT INTO `django_migrations` VALUES (15, 'auth', '0010_alter_group_name_max_length', '2025-02-28 01:49:01.133283');
INSERT INTO `django_migrations` VALUES (16, 'auth', '0011_update_proxy_permissions', '2025-02-28 01:49:01.139372');
INSERT INTO `django_migrations` VALUES (17, 'auth', '0012_alter_user_first_name_max_length', '2025-02-28 01:49:01.173782');
INSERT INTO `django_migrations` VALUES (18, 'sessions', '0001_initial', '2025-02-28 01:49:01.197277');
INSERT INTO `django_migrations` VALUES (19, 'broadcast', '0001_initial', '2025-02-28 01:52:53.947476');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session`  (
  `session_key` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  INDEX `django_session_expire_date_a5c62663`(`expire_date`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_session
-- ----------------------------
INSERT INTO `django_session` VALUES ('kosdm1cgjeqed8xygya36iwir66ohv7l', '.eJxVjMEOwiAQRP-FsyEF3RY8eu83kIXdlaqhSWlPxn-XJj1o5jbvzbxVwG3NYau8hInUVRl1-u0ipieXHdADy33WaS7rMkW9K_qgVY8z8et2uH8HGWtuaxnkgpBEjDWSurMdXPQtrWew7EyKjfeI4MkRc7IAQlYETN8Re_X5AhF-OTM:1tnpW0:gS8xe4-vib0bN71ZSwKrHQ-aFi1wesxUDECZrPytE7E', '2025-03-14 01:50:12.209727');

SET FOREIGN_KEY_CHECKS = 1;
